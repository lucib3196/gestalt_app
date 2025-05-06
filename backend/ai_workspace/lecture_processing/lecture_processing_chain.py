import os
import json
import asyncio
from typing import List, Optional, Dict, Annotated, Any
import operator
from pydantic import BaseModel, Field
from IPython.display import Image, display  # type: ignore
from langchain import hub
from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy
from langgraph.channels.last_value import LastValue

from ..utils.helper import save_graph_visualization, pdf_to_image_persistent
from ..image_processing.ImageLLMProcessor import ImageLLMProcessor
from ..utils.models import (
    LectureRouter,
    ContentType,
    LectureSummary,
    StepTokenUsage,
    TokenUsage,
    Derivations,
    ConceptualQuestion,
    AllComputationalQuestions,
)


# State Models
class PDFInputState(BaseModel):
    """Represents the initial input state containing the uploaded PDF path."""

    pdf_path: str


class PDFProcessState(BaseModel):
    """State after processing PDF into images and analyzing lecture content."""

    pdf_path: str
    pdf_length: int = 0
    image_paths: List[str]
    lecture_content: Optional[LectureRouter]
    token_usage: Annotated[List[StepTokenUsage], operator.add] = Field(
        default_factory=list
    )
    lecture_summary: LectureSummary
    derivations: Optional[Derivations] = None
    conceputal_questions: Optional[ConceptualQuestion] = None
    computational_questions: Optional[AllComputationalQuestions] = None


class ProcessedLectureState(BaseModel):
    """Final state after all lecture content has been processed."""

    pdf_path: str


# Node Functions
async def upload_pdf(state: PDFInputState) -> PDFProcessState:
    """Uploads the PDF, converts pages to images, and prepares processing state."""
    pdf_directory = os.path.dirname(state.pdf_path)
    persistant_directory = os.path.join(pdf_directory, "lecture_images")
    os.makedirs(persistant_directory, exist_ok=True)

    image_paths = await pdf_to_image_persistent(state.pdf_path, persistant_directory)

    return {
        "pdf_length": len(image_paths),
        "image_paths": image_paths,
    }


async def initial_analysis(state: PDFProcessState) -> PDFProcessState:
    """Analyzes images to detect conceptual, computational, and mathematical elements."""
    prompt = """
    You are tasked with analyzing the following lecture content to determine the presence of the following elements:
    Conceptual Questions: Assess understanding of fundamental principles without detailed calculations.
    Computational Questions: Involve calculations or algorithmic procedures to find solutions.
    Mathematical Derivations: Step-by-step logical progressions starting from known principles to derive new results.
    """

    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=LectureRouter,
    )
    response = await image_extraction.send_arequest_raw(state.image_paths)

    # Extract and parse content
    ai_message = response["raw"]
    parsed_content = json.loads(ai_message.content)
    lecture_content = parsed_content["content"]

    # Extract token usage
    token_usage_data = ai_message.response_metadata.get("token_usage", {})

    return {
        "lecture_content": LectureRouter(content=lecture_content),
        "token_usage": [
            StepTokenUsage(
                step_name="initial_analysis", token_usage=TokenUsage(**token_usage_data)
            )
        ],
    }


def conditional_content_router(state: PDFProcessState) -> List[str]:
    """Routes based on detected lecture content types."""
    return state.lecture_content.content if state.lecture_content else []


async def extract_lecture_summary(state: PDFProcessState) -> PDFProcessState:
    """Generates a lecture summary based on analyzed lecture content."""
    lecture_summary_prompt = hub.pull("lecture-summary")
    image_extraction = ImageLLMProcessor(
        prompt=lecture_summary_prompt,
        include_raw=True,
        schema=LectureSummary,
    )
    response = await image_extraction.send_arequest_raw(state.image_paths)

    # Extract content
    ai_message = response["raw"]
    parsed_summary = LectureSummary(**json.loads(ai_message.content))

    # Extract token usage
    token_usage_data = ai_message.response_metadata.get("token_usage", {})
    state.token_usage.append(
        StepTokenUsage(
            step_name="generate_lecture_summary",
            token_usage=TokenUsage(**token_usage_data),
        )
    )

    # Update state
    state.lecture_summary = parsed_summary
    return {
        "lecture_summary": parsed_summary,
        "token_usage": [
            StepTokenUsage(
                step_name="generate_lecture_summary",
                token_usage=TokenUsage(**token_usage_data),
            )
        ],
    }


async def extracting_derivations(state: PDFProcessState) -> PDFProcessState:
    print("Extracting Derivations")
    derivation_extraction_prompt = hub.pull("extract-derivations")
    image_extraction = ImageLLMProcessor(
        prompt=derivation_extraction_prompt,
        include_raw=True,
        schema=Derivations,
    )
    response = await image_extraction.send_arequest_raw(state.image_paths)

    # Extract content
    ai_message = response["raw"]
    parsed_derivation = Derivations(**json.loads(ai_message.content))

    # Extract token usage
    token_usage_data = ai_message.response_metadata.get("token_usage", {})

    # Update state
    state.derivations = parsed_derivation
    return {
        "derivations": parsed_derivation,
        "token_usage": [
            StepTokenUsage(
                step_name="generate_lecture_summary",
                token_usage=TokenUsage(**token_usage_data),
            )
        ],
    }


async def extracting_concepetual_questions(state: PDFProcessState) -> PDFProcessState:

    return {
        "conceputal_questions": [
            ConceptualQuestion(question_name='Test',question="Conceptual question",requires_image=False,requires_external_data=False,source=None)
        ]
    }


async def extract_computational_questions(state: PDFProcessState) -> PDFProcessState:
    print("Extracting Computational Questions")
    prompt = hub.pull("extract-computational-questions")
    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=AllComputationalQuestions,
    )
    response = await image_extraction.send_arequest_raw(state.image_paths)

    # Extract content
    ai_message = response["raw"]
    computational_questions = AllComputationalQuestions(
        **json.loads(ai_message.content)
    )

    # Extract token usage
    token_usage_data = ai_message.response_metadata.get("token_usage", {})

    return {
        "computational_questions": computational_questions,
        "token_usage": [
            StepTokenUsage(
                step_name="extract_computational_questions",
                token_usage=TokenUsage(**token_usage_data),
            )
        ],
    }


async def generate_lecture_summary(state: PDFProcessState) -> PDFProcessState:
    print("Generating Lecture")


async def generate_gestalt_modules(state: PDFProcessState) -> PDFProcessState:
    print("Generating Gestalt Module")
    all_questions = state.computational_questions.dict()
    # print(f"These are all the questions {all_questions}")


graph = StateGraph(PDFProcessState, input=PDFInputState, output=PDFProcessState)

graph_nodes = [
    ("upload_pdf", upload_pdf),
    ("initial_analysis", initial_analysis),
    ("extract_lecture_summary", extract_lecture_summary),
    ("computational_question", extract_computational_questions),
    ("mathematical_derivations", extracting_derivations),
    ("conceptual_questions", extracting_concepetual_questions),
    ("generate_gestalt_modules", generate_gestalt_modules),
    ("generate_lecture_summary", generate_lecture_summary),
]
# Add nodes with retry policy.
for node_name, node_func in graph_nodes:
    graph.add_node(node_name, node_func, retry=RetryPolicy(max_attempts=1))


graph.add_edge(START, "upload_pdf")
graph.add_edge("upload_pdf", "initial_analysis")
graph.add_conditional_edges(
    "initial_analysis",
    conditional_content_router,
    [
        "conceptual_questions",
        "mathematical_derivations",
        "computational_question",
    ],
)
graph.add_edge("conceptual_questions", "generate_gestalt_modules")
graph.add_edge("computational_question", "generate_gestalt_modules")
graph.add_edge("generate_gestalt_modules", END)
graph.add_edge("mathematical_derivations", "generate_lecture_summary")


graph.add_edge("initial_analysis", "extract_lecture_summary")
graph.add_edge("extract_lecture_summary", "generate_lecture_summary")
graph.add_edge("generate_lecture_summary", END)

graph = graph.compile()


async def main():
    # Save the graph
    save_graph_visualization(
        graph,
        filename="ProcessLectureChain.png",
        base_path=os.path.dirname(os.path.abspath(__file__)),
    )
    # Run the graph
    pdf_path = r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lecture_02_03.pdf"

    pdf_path = PDFInputState(pdf_path=pdf_path)
    result: PDFProcessState = await graph.ainvoke(pdf_path)
    serializable_result = to_serializable(dict(result))
    print(serializable_result)
    with open('output.json', 'w') as f:
        json.dump(serializable_result, f, indent=4)
    


if __name__ == "__main__":
    asyncio.run(main())
