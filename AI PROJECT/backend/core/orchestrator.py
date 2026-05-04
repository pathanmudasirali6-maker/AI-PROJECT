from ai.retriever import get_context
from ai.generator import generate_decision
from schemas.decision import DecisionOutcome
from typing import Optional

async def process_query_orchestration(query: str, context_filters: Optional[dict] = None) -> DecisionOutcome:
    # 1. Retrieve Context (RAG)
    context_data = await get_context(query, context_filters)
    
    # 2. Generate Structured Outcome with Retries
    # Instructor handles Pydantic validation internally
    decision_data = await generate_decision(query, context_data)
    
    return decision_data
