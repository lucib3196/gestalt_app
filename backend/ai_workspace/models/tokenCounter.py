from pydantic import BaseModel, Field
from typing import Optional
# Token Usage Models
class CompletionTokenDetails(BaseModel):
    accepted_prediction_tokens: int
    audio_tokens: int
    reasoning_tokens: int
    rejected_prediction_tokens: int


class PromptTokenDetails(BaseModel):
    audio_tokens: int
    cached_tokens: int


class TokenUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: Optional[CompletionTokenDetails] = None
    prompt_tokens_details: Optional[PromptTokenDetails] = None


class StepTokenUsage(BaseModel):
    step_name: str = Field(..., description="The step in the chain")
    token_usage: TokenUsage