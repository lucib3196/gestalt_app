from pydantic import BaseModel, Field
from typing import List,Literal


class QueryList(BaseModel):
    queries: List[str] = Field(..., description="Search queries")


class BinaryScore(BaseModel):
    binary_score: Literal["yes", "no"]
