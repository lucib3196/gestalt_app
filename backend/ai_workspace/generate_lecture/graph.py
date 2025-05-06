import os
import json
import asyncio
from datetime import date, datetime
from typing import List, Optional, Annotated, Union
import operator

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy
from langchain_openai import ChatOpenAI

from ..utils.helper import save_graph_visualization, pdf_to_image_persistent
from ..image_processing.ImageLLMProcessor import ImageLLMProcessor
from ..utils.models import LectureRouter, StepTokenUsage, TokenUsage
from .generate_summary import generate_lecture_summary, LectureSummary
from .extract_derivation import extract_derivations, Derivations
from .extract_questions import (
    extract_computational_questions,
    ComputatationalQuestions,
    ComputationalQuestion,
)
from langchain_core.prompts import ChatPromptTemplate
from ..agents.engineering_codegen.code_generator import (
    QuestionPayload,
    QuestionPackage,
)
from ..agents.engineering_codegen.code_generator import (
    compiled_graph as gestalt_generator,
)


FAST_MODEL = "gpt-4o-mini"
LONG_CONTEXT_MODEL = "gpt-4o"

fast_llm = ChatOpenAI(model=FAST_MODEL)
long_context_llm = ChatOpenAI(model=LONG_CONTEXT_MODEL)


def to_serializable(obj):
    """
    Recursively convert Pydantic models to serializable Python dicts.
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    return obj


class FinalLecture(BaseModel):
    lecture: str


class LectureMetadata(BaseModel):
    lecture_title: str
    course_name: str
    course_code: Union[str, int]
    instructor_name: str
    lecture_date: Optional[date] = None  # YYYY-MM-DD format
    processed_data: datetime = Field(default_factory=datetime.now)
    semester: str

    @property
    def as_str(self) -> str:
        date_str = f"Lecture Date: {self.lecture_date}" if self.lecture_date else ""
        return (
            f"Course: {self.course_name}-{self.course_code}  "
            f"Instructor: {self.instructor_name}  "
            f"{date_str}  Term: {self.semester}"
        )


class LecturePayload(BaseModel):
    base_lecture: str = Field(
        ..., title="A base lecture just the concatenation of the lecture and derivation"
    )
    final_lecture: str = Field(..., title="A cleaned up lecture using LLM processing")


class ProcessedLecture(BaseModel):
    lecture_images: List[str]
    pdf_path: Optional[str]
    lecture_metadata: Optional[LectureMetadata]
    token_usage: Annotated[List[StepTokenUsage], operator.add] = Field(
        default_factory=list
    )
    lecture_content: Optional[LectureRouter] = None
    lecture_summary: Optional[LectureSummary] = None
    derivations: Optional[Derivations] = None
    computational_questions: Optional[ComputationalQuestion] = None
    lecture_payload: Optional[LecturePayload] = None
    gestalt_packages: Optional[List[QuestionPackage]] = None


async def initial_analysis(state: ProcessedLecture):
    """
    Analyze images to detect conceptual, computational, and mathematical elements.
    """
    prompt = """
    You are tasked with analyzing the following lecture content to determine the presence of:
    - Conceptual Questions
    - Computational Questions
    - Mathematical Derivations
    """

    processor = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=LectureRouter,
    )
    response = await processor.send_arequest_raw(state.lecture_images)

    raw = response["raw"]
    parsed = json.loads(raw.content)
    content = parsed.get("content", [])
    token_data = raw.response_metadata.get("token_usage", {})

    return {
        "lecture_content": LectureRouter(content=content),
        "token_usage": [
            StepTokenUsage(
                step_name="initial_analysis",
                token_usage=TokenUsage(**token_data),
            )
        ],
    }


def conditional_content_router(state: ProcessedLecture):
    """
    Determine which lecture content types were detected.
    """
    print(state.lecture_content.content)
    return state.lecture_content.content if state.lecture_content else []


async def extract_lecture_summary(state: ProcessedLecture):
    result = await generate_lecture_summary(state.lecture_images)
    return {
        "lecture_summary": result.get("lecture_summary"),
        "token_usage": result.get("token_usage"),
    }


async def extract_derivations_lecture(state: ProcessedLecture):
    result = await extract_derivations(image_paths=state.lecture_images)
    return {
        "derivations": result.get("derivations"),
        "token_usage": result.get("token_usage"),
    }


async def extract_computational_questions_lecture(state: ProcessedLecture):
    questions = await extract_computational_questions(state.lecture_images)
    if not questions:
        raise RuntimeError("Condition unmet—retrying")
    return {
        "computational_questions": questions.get("computational_questions"),
        "token_usage": questions.get("token_usage"),
    }


async def extracting_conceptual_questions(state: ProcessedLecture):
    # raise NotImplementedError("Conceptual question extraction not implemented yet.")
    pass


async def generate_gestalt_modules(state: ProcessedLecture):
    all_questions: List[ComputationalQuestion] = state.computational_questions.questions
    initial_metadata = {
        "createdBy": "lberm007@ucr.edu",
        "qtype": "num",
        "nSteps": 1,
        "updatedBy": "",
        "difficulty": 1,
        "codelang": "javascript",
        "reviewed": "False",
        "ai_generated": "True",
    }

    question_payloads = [
        QuestionPayload(
            question=question.question,
            solution_guide=question.as_str,
        )
        for question in all_questions
    ]

    format_tasks = [
        gestalt_generator.ainvoke(
            {"question_payload": payload, "initial_metadata": initial_metadata}
        )
        for payload in question_payloads
    ]
    gestalt_packages = await asyncio.gather(*format_tasks)

    return {"gestalt_packages": gestalt_packages}


async def finalize_lecture(state: ProcessedLecture) -> dict:
    base_lecture = state.lecture_summary.as_str
    base_derivations = state.derivations.as_str
    lecture_meta = state.lecture_metadata.as_str if state.lecture_metadata else None

    prompt = f"""
    You are an expert Wikipedia author and a university professor. Your task is to write a comprehensive, wiki-style lecture article in Markdown, strictly following Wikipedia’s formatting guidelines.

    You’ll be provided with:
    - **base_lecture**: A summary of the lecture’s content.
    - **base_derivations**: All mathematical derivations from the lecture.

    Requirements:
    1. **Structure & Flow**
       - Organize the material into clear, logical sections.
       - Include a **Table of Contents** at the top, with links to each section.
    2. **Content Cleanup**
       - Retain every step of the provided derivations; apply only minor editorial fixes (grammar, clarity).
       - Expand on the summary where needed for coherence and completeness.
    3. **Style**
       - Follow Wikipedia’s tone, style, and section conventions (lead paragraph, headings, internal links).
       - Use Markdown syntax for headings, lists, equations, and links.
       - For math, use `$$` for block math and `$` for inline math.

    base_lecture: {base_lecture}

    base_derivations: {base_derivations}
   """
    if lecture_meta:
        prompt += f"\n\nAdditionally, include course info: {lecture_meta}"

    structured_llm: FinalLecture = long_context_llm.with_structured_output(FinalLecture)
    result = await structured_llm.ainvoke(prompt)
    return {
        "lecture_payload": {
            "base_lecture": base_lecture + "\n\n" + base_derivations,
            "final_lecture": result.lecture,
        }
    }


# Build the processing graph
graph = StateGraph(ProcessedLecture)
nodes = [
    ("initial_analysis", initial_analysis),
    ("extract_lecture_summary", extract_lecture_summary),
    ("computational_question", extract_computational_questions_lecture),
    ("mathematical_derivations", extract_derivations_lecture),
    ("conceptual_questions", extracting_conceptual_questions),
    ("generate_gestalt_modules", generate_gestalt_modules),
    ("finalize_lecture", finalize_lecture),
]

graph.add_conditional_edges(
    "initial_analysis",
    conditional_content_router,
    ["conceptual_questions", "mathematical_derivations", "computational_question"],
)


def ensure_question_router(state: ProcessedLecture) -> str:
    """
    Determine which lecture content type was detected.
    Returns either 'computational_questions' or 'conceptual_questions'.
    """
    # if there's a computational question, go there
    if state.computational_questions.question is not None:
        return "computational_questions"

    # otherwise, if there's a conceptual question, go there
    # if state.conceptual_questions.question is not None:
    #     return "conceptual_questions"

graph.add_conditional_edges(
    "generate_gestalt_modules",
    ensure_question_router,
    "computational_question"
)

for name, func in nodes:
    graph.add_node(name, func, retry=RetryPolicy(max_attempts=2))

graph.add_edge(START, "initial_analysis")
graph.add_edge("initial_analysis", "extract_lecture_summary")
graph.add_edge("conceptual_questions", "generate_gestalt_modules")
graph.add_edge("computational_question", "generate_gestalt_modules")
graph.add_edge("generate_gestalt_modules", END)
graph.add_edge("mathematical_derivations", "finalize_lecture")
graph.add_edge("extract_lecture_summary", "finalize_lecture")
graph.add_edge("finalize_lecture", END)
graph = graph.compile()


async def main():
    # Visualize graph
    save_graph_visualization(
        graph,
        filename="ProcessLectureChain.png",
        base_path=os.path.dirname(os.path.abspath(__file__)),
    )

    # pdf_path = r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lecture_02_03.pdf"
    # output_dir = os.path.join(os.path.dirname(pdf_path), "lecture_images")
    # os.makedirs(output_dir, exist_ok=True)

    # image_paths = await pdf_to_image_persistent(pdf_path, output_dir)
    # metadata = LectureMetadata(
    #     lecture_title="Buoyancy",
    #     course_name="Transport Phenomena",
    #     course_code=135,
    #     instructor_name="Sundararajan Venkatadriagaram",
    #     semester="Winter 2024",
    # )

    # input_data = ProcessedLecture(
    #     lecture_images=image_paths,
    #     pdf_path=pdf_path,
    #     lecture_metadata=metadata,
    # )

    # # Execute the graph
    # result: ProcessedLecture = await graph.ainvoke(input_data)

    # # Print final markdown

    # # Save full state
    # serializable = to_serializable(result)
    # with open(
    #     os.path.join(os.path.dirname(__file__), "lecture_data.json"),
    #     "w",
    # ) as f:
    #     json.dump(serializable, f, indent=4, default=str)


    print("Saved as my_lecture.md")


if __name__ == "__main__":
    asyncio.run(main())
