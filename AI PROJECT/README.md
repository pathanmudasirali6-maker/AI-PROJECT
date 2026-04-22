# InsightForge – AI Decision Intelligence Platform

InsightForge is an end-to-end AI system designed to resolve decision paralysis by transforming unstructured web data and internal documents into strict, confident, structured comparisons.

## Architecture
- **Frontend:** Next.js (App Router) + TailwindCSS
- **Backend:** FastAPI + Pydantic + Instructor
- **AI Core:** GPT-4o-mini structured via Instructor for deterministic schemas, with custom retry logic and RAG-based factual retrieval.

## Data Flow
1. User enters a query into the Next.js Dashboard.
2. The UI sends a JSON payload to the FastAPI `/api/v1/query` endpoint.
3. The orchestrator calls the RAG Retriever to pull factual constraints based on the query.
4. The orchestrator passes the context and query to the LLM Generator (via Instructor).
5. The LLM generates the `DecisionOutcome`. If validation fails, Instructor automatically retries with the exact validation error appended.
6. The frontend renders the comparison grid and strict confidence scores.

## Evaluation & Reliability Strategy
- **RAG for Hallucination Reduction:** By feeding context explicitly into the model, we ground responses in reality.
- **Pydantic Schema Enforcement:** Enforces rigorous JSON keys for `ComparisonFeature` metrics.
- **Retry Middleware:** Automatically traps `ValidationError` exceptions and passes them as feedback to the LLM.

## Hackathon Pitch Script (5-Minute)
*See `DOCUMENTATION.md` for full pitch script.*

## Deployment
- **Backend:** Render (see `backend/render.yaml` script setup).
- **Frontend:** Vercel (connect GitHub and configure `NEXT_PUBLIC_API_URL` environment variable).
