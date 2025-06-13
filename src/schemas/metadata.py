from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class PreRequisites(BaseModel):
    engineering: Optional[List[str]] = Field(
        None,
        title="Engineering Prerequisites",
        description="A list of Engineering-specific topics or skills that learners should have mastered before attempting this question.",
    )
    math: Optional[List[str]] = Field(
        None,
        title="Math Prerequisites",
        description="A list of Math-specific topics or skills that learners should have mastered before attempting this question.",
    )


class QuestionMetadata(BaseModel):
    title: str = Field(..., description="A concise title summarizing the question.")
    tags: List[str] = Field(
        ..., description="A list of keywords for categorization and filtering."
    )
    prereqs: Optional[PreRequisites] = Field(
        None,
        description="Math or Engineering prerequisites that are required to understand and solve the problem.",
    )
    sAdaptive: Literal["true", "false"] = Field(
        ...,
        description="Whether the question is adaptive (requires computation and a backend) or non-adaptive (e.g., multiple choice).",
    )
