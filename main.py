"""FastAPI application entry point and route handlers."""

import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from config import settings
from models.request import QueryRequest
from models.response import ComparisonResult, Comparison, ErrorResponse
from models.internal import AnalyzedQuery
from services import (
    QueryAnalyzer,
    RAGRetriever,
    LLMOrchestrator,
    Validator,
    ConfidenceScorer,
    QueryCache
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


# Initialize services (global for reuse across requests)
query_analyzer: Optional[QueryAnalyzer] = None
rag_retriever: Optional[RAGRetriever] = None
llm_orchestrator: Optional[LLMOrchestrator] = None
validator: Optional[Validator] = None
confidence_scorer: Optional[ConfidenceScorer] = None
cache: Optional[QueryCache] = None


def initialize_services() -> None:
    """Ensure all singleton services are initialized.

    This is safe to call multiple times and helps keep the app working even if
    lifespan startup events are skipped (such as in some test runners).
    """
    global query_analyzer, rag_retriever, llm_orchestrator, validator, confidence_scorer, cache

    if query_analyzer is not None and rag_retriever is not None:
        return

    logger.info("Initializing services...")
    query_analyzer = QueryAnalyzer()
    rag_retriever = RAGRetriever()
    llm_orchestrator = LLMOrchestrator()
    validator = Validator()
    confidence_scorer = ConfidenceScorer()
    cache = QueryCache() if settings.cache_enabled else None

    logger.info("Service initialization complete")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan event handler for startup/shutdown."""
    # Startup
    logger.info("=== InsightForge Backend Starting ===")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Model: {settings.llm_model}")
    logger.info(f"Debug: {settings.debug}")

    initialize_services()

    yield

    # Shutdown
    logger.info("=== InsightForge Backend Shutting Down ===")


# Create FastAPI app
app = FastAPI(
    title="InsightForge API",
    description="AI Decision Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "insightforge-backend",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.post("/api/query", response_model=ComparisonResult)
async def query_endpoint(request: QueryRequest):
    """
    Main endpoint: Accept a query and return structured comparison.
    
    Args:
        request: QueryRequest with query, entities, and criteria
    
    Returns:
        Structured comparison result with confidence and sources
    
    Raises:
        HTTPException on validation or processing errors
    """
    # Ensure services are initialized (supports test clients and edge runtimes)
    initialize_services()

    trace_id = str(uuid.uuid4())
    start_time = asyncio.get_event_loop().time()
    
    logger.info(f"[{trace_id}] Incoming query: {request.query}")
    
    try:
        # Step 1: Analyze query
        logger.debug(f"[{trace_id}] Step 1: Analyzing query")
        try:
            analyzed_query = query_analyzer.analyze(
                request.query,
                request.entities,
                request.criteria
            )
        except Exception as e:
            logger.error(f"[{trace_id}] Query analysis failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query analysis failed: " + str(e)
            )
        
        # Step 1a: Check cache if enabled
        cache_key = None
        result_from_cache = None
        if settings.cache_enabled and cache is not None:
            cache_key = cache.make_key(
                analyzed_query.normalized_query,
                analyzed_query.entities,
                analyzed_query.criteria
            )
            result_from_cache = cache.get(cache_key)
            if result_from_cache:
                logger.info(f"[{trace_id}] Returning cached response")
                return result_from_cache
        
        # Step 2: Retrieve context
        logger.debug(f"[{trace_id}] Step 2: Retrieving context via RAG")
        try:
            retrieval_result = rag_retriever.retrieve(analyzed_query, request.max_sources)
        except Exception as e:
            logger.error(f"[{trace_id}] Retrieval failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Context retrieval failed"
            )
        
        # Step 3: Generate comparison with retries
        logger.debug(f"[{trace_id}] Step 3: Generating comparison with retries")
        max_attempts = settings.max_retries
        last_error = None
        generated_response = None
        
        for attempt in range(1, max_attempts + 1):
            try:
                llm_response = llm_orchestrator.generate_comparison(
                    analyzed_query,
                    retrieval_result
                )
                
                if llm_response.is_valid and llm_response.parsed_json:
                    generated_response = llm_response.parsed_json
                    logger.debug(f"[{trace_id}] LLM generation succeeded on attempt {attempt}")
                    break
                else:
                    last_error = llm_response.parse_error
                    logger.warning(
                        f"[{trace_id}] LLM generation failed on attempt {attempt}: {last_error}"
                    )
                    
                    if attempt < max_attempts:
                        logger.info(f"[{trace_id}] Retrying... (attempt {attempt + 1}/{max_attempts})")
                        await asyncio.sleep(0.5)
            
            except Exception as e:
                last_error = str(e)
                logger.warning(f"[{trace_id}] Error on attempt {attempt}: {str(e)}")
                if attempt < max_attempts:
                    await asyncio.sleep(0.5)
        
        if not generated_response:
            logger.error(f"[{trace_id}] Generation failed after {max_attempts} attempts")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate comparison after retries"
            )
        
        # Step 4: Validate response
        logger.debug(f"[{trace_id}] Step 4: Validating response")
        try:
            validated_response = validator.validate_response(generated_response)
        except Exception as e:
            logger.error(f"[{trace_id}] Validation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Response validation failed"
            )
        
        # Step 5: Calculate confidence score
        logger.debug(f"[{trace_id}] Step 5: Calculating confidence score")
        confidence = confidence_scorer.calculate_score(
            retrieval_result.chunks,
            validated_response,
            analyzed_query
        )
        
        # Step 6: Build final response
        logger.debug(f"[{trace_id}] Step 6: Building final response")
        elapsed_time = (asyncio.get_event_loop().time() - start_time) * 1000
        
        comparison = Comparison(
            id=f"cmp_{trace_id}",
            timestamp=datetime.utcnow(),
            query_summary=analyzed_query.normalized_query,
            criteria=validated_response.get("criteria", [])
        )
        
        # Build sources list from retrieval chunks
        sources = []
        seen_sources = {}
        
        for idx, chunk in enumerate(retrieval_result.chunks):
            source_key = chunk.source_url
            
            if source_key not in seen_sources:
                from models.response import Source
                source = Source(
                    id=chunk.source_id,
                    title=chunk.source_title,
                    url=chunk.source_url,
                    relevance=chunk.relevance,
                    type=chunk.source_type,
                    citations=[],
                    retrieved_at=datetime.utcnow()
                )
                sources.append(source)
                seen_sources[source_key] = len(sources) - 1
        
        # Import required models for response
        from models.response import Metadata
        
        # Determine low confidence flag using configured threshold
        low_conf = False
        if settings.confidence_threshold is not None:
            low_conf = confidence.score < settings.confidence_threshold
        
        metadata = Metadata(
            generation_time_ms=int(elapsed_time),
            retrieval_chunks=retrieval_result.total_chunks,
            retry_count=max_attempts - 1,  # Actual retries needed
            model_used=settings.llm_model,
            version="1.0",
            cached=bool(result_from_cache),
            prompt_variant=llm_orchestrator.prompt_variant,
            confidence_threshold=settings.confidence_threshold,
            low_confidence=low_conf
        )
        
        result = ComparisonResult(
            comparison=comparison,
            confidence=confidence,
            sources=sources,
            metadata=metadata
        )
        
        # Store in cache for future identical queries
        if settings.cache_enabled and cache is not None and not result_from_cache and cache_key:
            cache.set(cache_key, result)
        
        logger.info(f"[{trace_id}] Query processed successfully in {elapsed_time:.0f}ms")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{trace_id}] Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/api/status")
async def status_endpoint():
    """Check API status and configuration."""
    initialize_services()

    return {
        "status": "operational",
        "services": {
            "query_analyzer": query_analyzer is not None,
            "rag_retriever": rag_retriever is not None,
            "llm_orchestrator": llm_orchestrator is not None,
            "validator": validator is not None,
            "confidence_scorer": confidence_scorer is not None,
        },
        "config": {
            "model": settings.llm_model,
            "max_retries": settings.max_retries,
            "embedding_model": settings.embedding_model,
        }
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return {
        "code": "HTTP_ERROR",
        "message": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
