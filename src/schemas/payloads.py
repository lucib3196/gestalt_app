from typing import Literal, List, Optional, Any, Union
from pydantic import BaseModel, Field
from .generic import Section

# --- Metadata Models ---


class InitialMetadata(BaseModel):
    createdBy: str
    qtype: str
    nSteps: int
    updatedBy: str
    codelang: str
    reviewed: Literal["True", "False"]
    ai_generated: Literal["True", "False"]


class QuestionMetadata(BaseModel):
    title: str = Field(..., description="A concise title summarizing the question.")
    question: str = Field(
        ..., description="The main question text that students are expected to answer."
    )
    stem: str = Field(
        ..., description="Background or scenario text that frames the question."
    )
    topic: str = Field(
        ..., description="The subject area or category this question belongs to."
    )
    tags: List[str] = Field(
        ..., description="A list of keywords for categorization and filtering."
    )
    prereqs: Optional[List[str]] = Field(
        None,
        description="Math or Engineering prerequisites that are required to understand and solve the problem.",
    )
    isAdaptive: Literal["True", "False"] = Field(
        ...,
        description="Whether the question is adaptive (requires computation and a backend) or non-adaptive (e.g., multiple choice).",
    )


# --- Question Model ---


class Question(BaseModel):
    question: str = Field(
        ...,
        title="Question",
        description="A fully formed question. It should be complete and clearly stated.",
    )
    source: Optional[Union[str, int]] = Field(
        None,
        title="Source",
        description="The source from which the question was extracted. Ideally, this is a page number or identifier from lecture content or a textbook.",
    )
    requires_external_data: Optional[bool] = Field(
        None,
        title="Requires External Data",
        description="Whether the question depends on external data such as tables, charts, or datasets to be solved.",
    )
    requires_image: Optional[bool] = Field(
        None,
        title="Requires Image",
        description="Whether an image is required to fully understand the question.",
    )
    completeness: Optional[bool] = Field(
        None,
        title="Completeness",
        description="Whether the question or derivation is complete or requires additional steps.",
    )
    additional_information: Optional[str] = Field(
        None,
        title="Additional instructions for code generation",
        description="Additional instructiosn for code generation",
    )
    solution: Optional[List[Section]] = Field(
        default_factory=list,
        title="Titles and descriptions for each solution step",
        description="The solution guide of the question any math should be delimited by $$ for block level and $ for inline ",
    )

    @property
    def as_str(self) -> str:
        solution_steps = (
            "\n\n".join(solution.as_str for solution in self.solution)
            if self.solution
            else None
        )
        source = f"\nSource: {self.source}" if self.source else ""
        return f"{self.question}\n{source}\n\n{solution_steps}".strip()

    @property
    def solution_as_str(self) -> str:
        return (
            "\n\n".join(solution.as_str for solution in self.solution)
            if self.solution
            else ""
        )


# --- Files Data Model ---
class FilesData(BaseModel):
    """Holds the generated file contents related to a question."""

    question_html: str = ""
    server_js: str = ""
    server_py: str = ""
    solution_html: str = ""
    metadata: dict[str, Any] = {}


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


class LectureSummary(BaseModel):

    lecture_name: str = Field(
        ...,
        title="Title of the lecture",
        description="A title for the lecture should describe the main ideas that the lecture covers",
    )
    summary: str = Field(
        ...,
        title="A consise and to the point summary of the lecture and what it convered",
        description="A summary of the lecture",
    )
    key_takeaways: List[Section] = Field(
        ...,
        description="Titles and descriptions for a section on the iportant principles, laws, formulas introduced.",
        title="Title and sections of the key takeaways",
    )
    learning_objectives: List[Section] = Field(
        ...,
        description="Titles and Section of what the students should understand from the lecture",
    )
    technical_concepts: List[Section] = Field(
        ...,
        description="Titles and Section of the technical concepts introduced including definitions, laws and principles, fundamental equations etc",
    )

    @property
    def as_str(self) -> str:
        key_takeaways = "\n\n".join(
            key_takeaway.as_str for key_takeaway in self.learning_objectives
        )
        learning_objectives = "\n\n".join(
            learning_objective.as_str for learning_objective in self.learning_objectives
        )
        technical_concepts = "\n\n".join(
            technical_concept.as_str for technical_concept in self.technical_concepts
        )
        return f"# {self.lecture_name}\n {self.summary}  \n\n{key_takeaways}\n\n{learning_objectives}\n\n{technical_concepts}".strip()
