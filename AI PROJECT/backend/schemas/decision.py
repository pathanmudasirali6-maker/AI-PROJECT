from pydantic import BaseModel, Field
from typing import List, Optional

class ComparisonFeature(BaseModel):
    feature_name: str
    option_a_detail: str
    option_b_detail: str
    winner: Optional[str] = Field(None, description="Which option wins this feature, or 'Tie'")

class DecisionOutcome(BaseModel):
    summary: str
    comparison_table: List[ComparisonFeature]
    confidence_score: int = Field(..., ge=0, le=100, description="Confidence in the recommendation")
    sources_cited: List[str]
    recommendation: str

class QueryRequest(BaseModel):
    query: str
    context_filters: Optional[dict] = None
