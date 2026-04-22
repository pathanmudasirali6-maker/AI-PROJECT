from fastapi import APIRouter, HTTPException
from schemas.decision import QueryRequest, DecisionOutcome
from core.orchestrator import process_query_orchestration

router = APIRouter()

@router.post("/api/v1/query", response_model=DecisionOutcome)
async def process_decision_query(request: QueryRequest):
    try:
        decision_data = await process_query_orchestration(request.query, request.context_filters)
        return decision_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
