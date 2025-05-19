from pydantic import BaseModel, Field
from typing import List, Literal, Optional,Union


ContentType = Literal[
    "conceptual_questions", "mathematical_derivations", "computational_question"
]


class LectureRouter(BaseModel):
    content: list[ContentType]


# Lecture Summary
class KeyWord(BaseModel):
    keyword: str = Field(..., description="Keyword")
    description: str = Field(
        ...,
        description="Description of the keyword. Use LaTeX for any mathematical symbols or equations.",
    )


class LectureSummary(BaseModel):
    lecture_name: str = Field(
        ..., description="A concise and descriptive title of the lecture"
    )
    summary: str = Field(
        ...,
        description="Summary of the lecture. Use LaTeX for any mathematical symbols or equations.",
    )
    key_concepts: List[KeyWord] = Field(
        ..., description="List of key concepts covered in the lecture."
    )
    foundational_concepts: List[KeyWord] = Field(
        ..., description="List of prerequisite concepts for the lecture."
    )
    search_keywords: List[str] = Field(
        ..., description="Relevant search queries for additional references."
    )


class ConceptualQuestion(BaseModel):
    question_name: str = Field(...,description="The name of the question")
    question: str = Field(
        ...,
        description=(
            "Question presented in the lecture slide or image. Must be the full extracted question. "
            "Format any mathematical symbols or equations using LaTeX."
        ),
    )
    requires_image: bool = Field(
        ..., description="Wether the question requires an image to fully understand"
    )
    requires_external_data: bool = Field(
        ...,
        description="Wether the question requires external data including tables, charts, datasets required to solve the question",
    )
    source: Union[str,int,None] = Field(
        ...,description='An identifier of where the question came from it can be a page number if it is present in the document'
    )


class ComputationalQuestion(ConceptualQuestion):
    solution: str = Field(
        ...,
        description=(
            "A detailed solution with steps for the computational question, using LaTeX for formatting "
            "any mathematical symbols or equations."
        ),
    )
    complete: bool = Field(
        ...,
        description=(
            "Indicates if the question is completed with the solutions. If `false`, the `solution` field can be empty."
        ),
    )

class AllComputationalQuestions(BaseModel):
    computational_questions: List[ComputationalQuestion]

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


# Extract Derivations
class Derivation(BaseModel):
    """
    Represents a single derivation extracted from lecture content.

    Attributes:
        derivation_name (str): The name of the derivation and what it aims to demonstrate.
        derivation_steps (str): A list of steps involved in the derivation, each step explained and formatted using LaTeX for mathematical symbols or equations.
        complete_derivation (bool): Indicates if the derivation is complete. Returns True if complete, else False.
    """

    derivation_name: str = Field(
        ..., description="The name of the derivation and what it aims to demonstrate."
    )
    derivation_steps: str = Field(
        ...,
        description=(
            "A list of steps involved in the derivation, each step explained and formatted using LaTeX "
            "for mathematical symbols or equations. For any mathematical symbols, use LaTeX and delimit using "
            "`$` for inline math and `$$` for block-level math."
        ),
    )
    complete_derivation: bool = Field(
        ..., description="If the derivation is complete, return True; else False."
    )


class Derivations(BaseModel):
    """
    Container for multiple derivations extracted from lecture content.

    Attributes:
        derivations (List[Derivation]): A list of extracted derivations.
    """

    derivations: List[Derivation] = Field(
        ..., description="A list of extracted derivations."
    )
