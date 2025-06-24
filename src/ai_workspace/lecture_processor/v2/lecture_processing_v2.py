import os
import asyncio
import json
import time

from typing import List, Literal, Optional, Annotated
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy
from typing import Union
from ai_workspace.agentsv2.image_processing.ImageLLMProcessor import ImageLLMProcessor
from ai_workspace.utils import (
    extract_token_usage,
    parse_structured,
    pdf_to_image_persistent,
    to_serializable,
    save_graph_visualization,
)
from ai_workspace.extraction.v1.extract_content_ranges import (
    extract_derivation_ranges,
    extract_question_ranges,
)

from ai_workspace.agentsv2.code_generator.ver2.code_generator import (
    compiled_graph as gestalt_generator,
    CodeGenInput,
    CodeGenState,
)

from ai_workspace.extraction.v1.extract_derivations import (
    extract_derivations,
    Derivations,
    Derivation,
)
from ai_workspace.extraction.v1.extract_questions import extract_questions, AllQuestion
from ai_workspace.extraction.v1.extract_summary import extract_summary
from ai_workspace.models.tokenCounter import TokenUsage, StepTokenUsage
from ai_workspace.utils.reducers import reduce_token_usage
from schemas import LectureSummary

FAST_MODEL = "gpt-4o-mini"
LONG_CONTEXT_MODEL = "gpt-4.1-2025-04-14"

fast_llm = ChatOpenAI(model=FAST_MODEL)
long_context_llm = ChatOpenAI(model=LONG_CONTEXT_MODEL)


def merge_all_questions(all_q_list: List[AllQuestion]) -> AllQuestion:
    merged = AllQuestion(questions=[])
    for aq in all_q_list:
        merged.questions += aq.questions
    return merged


def merge_all_derivatons(derivations: List[Derivation]) -> Derivations:
    return Derivations(all_derivations=derivations)


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


# Routing
ContentType = Literal["extract_lecture_derivations", "extract_lecture_questions"]


class LectureRouter(BaseModel):
    content: list[ContentType]


from pydantic import BaseModel, Field
from typing import Optional, List, Annotated


# State Models
class LectureInputState(BaseModel):
    image_paths: list[str] = Field(
        ...,
        title="Image Paths",
        description="List of file paths pointing to the lecture images to be processed.",
    )
    seperate_image: bool = Field(
        False,
        title="Separate Image Flag",
        description="Whether to treat each image separately for processing (True) or as a continuous lecture (False).",
    )
    web_search: Optional[bool] = Field(False)
    lecture_metadata: Optional[LectureMetadata] = Field(
        None,
        title="Lecture Metadata",
        description="Optional metadata about the lecture, such as course title or instructor.",
    )


class LectureIntermediate(BaseModel):
    image_paths: list[str] = Field(
        ...,
        title="Image Paths",
        description="List of image paths from the uploaded lecture content.",
    )
    seperate_image: bool = Field(
        False,
        title="Separate Image Flag",
        description="Flag indicating if image processing should occur separately per image.",
    )
    lecture_content: Optional["LectureRouter"] = Field(
        None,
        title="Lecture Content",
        description="Structured representation of extracted lecture components such as questions, derivations, etc.",
    )
    lecture_summary: Optional["LectureSummary"] = Field(
        None,
        title="Lecture Summary",
        description="Generated summary of the lecture highlighting key concepts and objectives.",
    )
    lecture_derivations: Optional["Derivations"] = Field(
        None,
        title="Lecture Derivations",
        description="Extracted or generated derivations that appear within the lecture.",
    )
    lecture_questions: Optional["AllQuestion"] = Field(
        None,
        title="Lecture Questions",
        description="Structured question content extracted or generated from the lecture.",
    )
    final_lecture: Optional[str] = Field(
        None,
        title="Final Lecture",
        description="Concatenated, formatted final lecture content as a single string.",
    )
    lecture_metadata: Optional["LectureMetadata"] = Field(
        None,
        title="Lecture Metadata",
        description="Optional additional metadata related to the lecture context.",
    )
    gestalt_modules: Optional[List["CodeGenState"]] = Field(
        None,
        title="Gestalt Modules",
        description="Optional list of generated modules containing supplemental educational content (e.g., code or simulations).",
    )
    token_usage: Annotated[List["StepTokenUsage"], reduce_token_usage] = Field(
        default_factory=list,
        title="Token Usage",
        description="List of token usage entries for tracking cost and performance.",
    )

    @field_validator("lecture_content", mode="before")
    @classmethod
    def _coerce_router(cls, v):
        if isinstance(v, list):
            return LectureRouter(content=v)
        return v


class ExtractedContent(BaseModel):
    lecture_content: Optional["LectureRouter"] = Field(
        None,
        title="Lecture Content",
        description="Parsed content extracted from the lecture images.",
    )
    lecture_summary: Optional["LectureSummary"] = Field(
        None,
        title="Lecture Summary",
        description="Summary section extracted or generated from the lecture.",
    )
    lecture_derivations: Optional["Derivations"] = Field(
        None,
        title="Lecture Derivations",
        description="Mathematical or conceptual derivations found in the lecture.",
    )
    lecture_questions: Optional["AllQuestion"] = Field(
        None,
        title="Lecture Questions",
        description="All extracted or generated questions from the lecture content.",
    )


class GeneratedLecture(BaseModel):
    final_lecture: str = Field(
        ...,
        title="Final Lecture",
        description="The complete formatted lecture output ready for display or export.",
    )
    lecture_base: str = Field(..., title="Lecture Base without final processing")
    derivation_str: Optional[str] = Field(
        None,
        title="Derivation Section",
        description="String version of the derivation section for HTML or markdown rendering.",
    )
    question_str: Optional[str] = Field(
        None,
        title="Question Section",
        description="String version of the question section for rendering purposes.",
    )


class LectureOutputState(BaseModel):
    lecture_metadata: Optional[LectureMetadata] = Field(None, title="Lecture Metadata")
    image_paths: list[str] = Field(
        ...,
        title="Image Paths",
        description="Paths to the lecture images that were processed.",
    )
    seperate_image: bool = Field(
        False,
        title="Separate Image Flag",
        description="Whether images were processed individually or as a batch.",
    )
    extracted_content: Optional[ExtractedContent] = Field(
        None,
        title="Extracted Content",
        description="Content that was extracted from the lecture, including summaries, derivations, and questions.",
    )
    generated_lecture: Optional[GeneratedLecture] = Field(
        None,
        title="Generated Lecture",
        description="The final structured lecture output ready for rendering or display.",
    )
    gestalt_modules: Optional[List[CodeGenState]] = Field(
        None,
        title="Gestalt Modules",
        description="List of modules generated from the lecture content.",
    )
    total_token_usage: List["StepTokenUsage"] = Field(
        ...,
        title="Total Token Usage",
        description="Total token usage across the entire processing pipeline.",
    )


async def content_analysis(state: LectureInputState):
    """
    Extracts questions from the provided image paths using an LLM processor.
    Retries up to `max_retries` times if response content is None or empty.
    """
    prompt = """
    You are tasked with analyzing the following lecture content to determine the presence of:
    - Conceptual/Computational Questions
    - Mathematical Derivations
    
    From here you will then route to the follwoing mapping
    - Conceptual/Computational Questions: `extract_lecture_questions`
    - Mathematical Derivations: `extract_lecture_derivations`
    
    """
    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=LectureRouter,
        model=LONG_CONTEXT_MODEL,
    )

    attempt = 0
    ai_message = None
    parsed = None
    max_retries = 1

    while attempt < max_retries:
        response = await image_extraction.send_arequest_raw(state.image_paths)
        ai_message = response.get("raw")
        try:
            parsed = parse_structured(LectureRouter, ai_message)
            break
        except Exception as e:
            print(f"Parsing failed on attempt {attempt + 1}: {e}")
        attempt += 1

    if not parsed:
        raise ValueError("Failed to parsed after retries.")

    token_usage = extract_token_usage(ai_message, "content_analysis")

    return {
        "lecture_content": parsed,
        "token_usage": [token_usage],
    }


def conditional_content_router(state: LectureIntermediate):
    """
    Determine which lecture content types were detected.
    """
    return state.lecture_content.content if state.lecture_content else []


async def extract_lecture_questions(state: LectureIntermediate):

    if state.seperate_image:
        question_response = await extract_question_ranges(state.image_paths)
        token_usage = question_response["token_usage"]
        sep_imagepaths = question_response["sep_imgpaths"]

        tasks = [extract_questions(sep_paths) for sep_paths in sep_imagepaths]
        responses: List[AllQuestion] = await asyncio.gather(*tasks)

        all_questions = []
        all_token_usage = []

        for r in responses:
            questions = r["questions"]
            token_usage: List[TokenUsage] = r["token_usage"]
            all_questions.append(questions)
            all_token_usage += token_usage
    else:
        response = await extract_questions(state.image_paths)
        all_questions = [response["questions"]]
        all_token_usage = response["token_usage"]

    return {
        "lecture_questions": merge_all_questions(all_questions),
        "token_usage": all_token_usage,
    }


async def generate_gestalt_modules(state: LectureIntermediate):

    all_questions = state.lecture_questions
    tasks = []
    for q in all_questions.questions:
        gestalt_geninput = CodeGenInput(question_payload=q)
        tasks.append(gestalt_generator.ainvoke(gestalt_geninput))
    response: List[CodeGenState] = await asyncio.gather(*tasks)
    return {"gestalt_modules": response}


async def extract_lecture_derivations(state: LectureIntermediate):
    all_token_usage = []

    if state.seperate_image:
        derivation_response = await extract_derivation_ranges(state.image_paths)
        sep_imagepaths = derivation_response["sep_imgpaths"]
        all_token_usage += derivation_response["token_usage"]

        tasks = [extract_derivations(sep_paths) for sep_paths in sep_imagepaths]
        responses = await asyncio.gather(*tasks)

        all_derivations = Derivations(all_derivations=[])
        for r in responses:
            derivations: Derivations = r["derivations"]
            token_usage: List[TokenUsage] = r["token_usage"]
            all_derivations.all_derivations = derivations.all_derivations
            all_token_usage += token_usage
    else:
        response = await extract_derivations(state.image_paths)
        all_derivations = response["derivations"]
        all_token_usage += response["token_usage"]

    return {
        "lecture_derivations": all_derivations,
        "token_usage": all_token_usage,
    }


async def extract_lecture_summary(state: LectureIntermediate):
    response = await extract_summary(state.image_paths)
    lecture_summary: LectureSummary = response["lecture_summary"]
    token_usage = response["token_usage"]
    return {"lecture_summary": lecture_summary, "token_usage": token_usage}


async def finalize_lecture(state: LectureIntermediate):

    class FinalLecture(BaseModel):
        lecture: str

    # Always include the lecture summary
    base_lecture = state.lecture_summary.as_str
    # Conditionally include derivations, questions, and metadata
    parts = [f"base_lecture: {base_lecture}"]
    if state.lecture_derivations:
        parts.append(f"base_derivations: {state.lecture_derivations.as_str}")
    if state.lecture_questions:
        parts.append(f"base_questions: {state.lecture_questions.as_str}")
    if state.lecture_metadata:
        parts.append(f"lecture_meta: {state.lecture_metadata.as_str}")

    # Join all provided parts into the prompt body
    prompt_body = "\n\n".join(parts)

    prompt = f"""
    You are a highly skilled university professor and experienced Wikipedia contributor. Your task is to generate a comprehensive, well-structured, and pedagogically sound educational article in Markdown format. The article must strictly follow Wikipedia’s tone, style, and formatting conventions.

    You will receive the following input data:
    - **base_lecture**: A high-level summary of the lecture content.
    { "- **base_derivations**: Detailed mathematical derivations presented during the lecture." if state.lecture_derivations else "" }
    { "- **base_questions**: A list of important lecture questions along with their solutions." if state.lecture_questions else "" }
    { "- **lecture_meta**: Supplementary metadata including course title, instructor, and date." if state.lecture_metadata else "" }

    ---

    ### ✅ Article Structure Guidelines (Designed for Student Learning)

    #### 1. Lead Section
    - Begin with a concise **lead paragraph** that introduces the topic, context, and its academic significance.
    - Define key terms early to reduce cognitive load and improve accessibility.

    #### 2. Table of Contents
    - Include a **Table of Contents** at the top with internal anchor links to each major section.
    - Ensure clear labeling of sections to facilitate quick navigation and review.

    #### 3. Main Content Sections
    Structure the article into clearly titled sections, ideally following this logical flow:

    1. **Introduction** – Expanded overview based on `base_lecture`.
    2. **Core Concepts** – Clarify major ideas using analogies, diagrams (if supported), and simplified explanations before diving into formal content.
    3. **Detailed Derivations** – (if applicable)
    4. **Worked Examples & Questions** – (if applicable)
    5. **Conclusion** – Summarize the key takeaways and link to advanced topics or applications.

    ---

    ### 🧮 Handling base_derivations (If Present)

    - Create a dedicated **“Mathematical Derivations”** section.
    - Present each derivation step-by-step, clearly labeled with subsection headers (e.g., "Derivation 1: Euler’s Formula").
    - Use `$$...$$` for block equations and `$...$` for inline math.
    - Briefly explain the **purpose** and **intuition** of each derivation before starting.
    - Add inline comments or footnotes for key assumptions or transformations.

    ---

    ### ❓ Handling base_questions (If Present)

    - Add a section titled **“Example Problems & Solutions”**.
    - For each question:
    - Use a callout block (e.g., Markdown blockquote or custom formatting) to clearly distinguish the question.
    - Follow immediately with a **step-by-step solution**, highlighting reasoning and common misconceptions.
    - Include brief notes on the educational value of the question (e.g., "This problem reinforces application of the chain rule in implicit functions").

    ### Handling lecture_meta (If Present)
    At the end of the beginning , include a Metadata Section with:

    Course Title

    Professor Name

    Lecture Date

    Institution

    Optionally include a short paragraph on the context of the lecture within the course (e.g., "This topic is part of Week 3 in the Differential Equations module, focusing on linear systems.").

    ### Writing & Formatting Requirements
    Use Markdown for all structural elements (headings, emphasis, lists, etc.).

    Follow an objective, neutral, and encyclopedic tone.

    Ensure all sections are clearly separated and labeled.

    Link key terms to internal concepts (e.g., use [Chain Rule](#chain-rule) to reference in-article anchors).

    Use the provided input to produce a student-friendly, structured article that is accurate, complete, and suitable for academic self-study or course integration.
    Ensure

    {prompt_body} """

    structured_llm = long_context_llm.with_structured_output(
        FinalLecture, include_raw=True
    )

    attempt = 0
    final_lecture = None
    ai_message = None
    max_retries = 1

    while attempt < max_retries and not final_lecture:
        response = await structured_llm.ainvoke(prompt)
        ai_message = response.get("raw")
        try:
            parsed = parse_structured(FinalLecture, ai_message)
            if parsed and parsed.lecture:
                final_lecture = parsed
                break
        except Exception as e:
            print(f"Parsing failed on attempt {attempt + 1}: {e}")
        attempt += 1

    token_usage = extract_token_usage(ai_message, "finalize_lecture")
    return {
        "final_lecture": final_lecture,
        "token_usage": [token_usage],
    }


async def finalze_package(state: LectureIntermediate) -> LectureOutputState:
    return LectureOutputState(
        lecture_metadata=state.lecture_metadata,
        image_paths=state.image_paths,
        seperate_image=state.seperate_image,
        generated_lecture=GeneratedLecture(
            final_lecture=state.final_lecture.lecture,
            lecture_base=state.lecture_summary.as_str,
            derivation_str=(
                state.lecture_derivations.as_str if state.lecture_derivations else None
            ),
            question_str=(
                state.lecture_questions.as_str if state.lecture_questions else None
            ),
        ),
        extracted_content=ExtractedContent(
            lecture_content=state.lecture_content,
            lecture_summary=state.lecture_summary,
            lecture_derivations=state.lecture_derivations,
            lecture_questions=state.lecture_questions,
        ),
        gestalt_modules=state.gestalt_modules,
        total_token_usage=state.token_usage,
    )


# Build the processing graph
graph = StateGraph(LectureOutputState, input=LectureInputState)
nodes = [
    ("content_analysis", content_analysis),
    ("extract_lecture_derivations", extract_lecture_derivations),
    ("extract_lecture_questions", extract_lecture_questions),
    ("extract_lecture_summary", extract_lecture_summary),
    ("finalze_package", finalze_package),
    ("finalize_lecture", finalize_lecture),
    ("generate_gestalt_modules", generate_gestalt_modules),
]

for name, func in nodes:
    graph.add_node(name, func, retry=RetryPolicy(max_attempts=2))

graph.add_conditional_edges(
    "content_analysis",
    conditional_content_router,
    ["extract_lecture_derivations", "extract_lecture_questions"],
)

graph.add_edge(START, "content_analysis")
graph.add_edge("content_analysis", "extract_lecture_summary")
graph.add_edge("extract_lecture_questions", "generate_gestalt_modules")
graph.add_edge("extract_lecture_questions", "finalize_lecture")
graph.add_edge("extract_lecture_summary", "finalize_lecture")
graph.add_edge("extract_lecture_derivations", "finalize_lecture")
graph.add_edge("generate_gestalt_modules", "finalze_package")
graph.add_edge("finalize_lecture", "finalze_package")

graph.add_edge("finalze_package", END)
graph = graph.compile()


async def main():
    # Removed redundant import of time
    start_time = time.time()
    save_graph_visualization(
        graph,
        filename="ProcessLectureChain.png",
        base_path=os.path.dirname(os.path.abspath(__file__)),
    )

    pdf_path = r"Lectures\Lec11-post.pdf"
    output_dir = os.path.join(os.path.dirname(pdf_path), "lecture_images")
    os.makedirs(output_dir, exist_ok=True)
    try:
        image_paths = await pdf_to_image_persistent(pdf_path, output_dir, annotate=True)
    except Exception as e:
        print(f"Error during PDF to image conversion: {e}")
        return
    metadata = LectureMetadata(
        lecture_title="Lecture 11",
        course_name="Dynamics",
        course_code=103,
        instructor_name="Thomas Stahovich",
        semester="Spring 2025",
    )

    graph_input = LectureInputState(
        image_paths=image_paths, lecture_metadata=metadata, seperate_image=True
    )
    result: LectureOutputState = await graph.ainvoke(graph_input)

    # Save full state
    serializable = to_serializable(result)
    with open(
        os.path.join(os.path.dirname(__file__), "processed_lecture.json"),
        "w",
    ) as f:
        json.dump(serializable, f, indent=4, default=str)
    print(f"total time: {time.time()-start_time}")


if __name__ == "__main__":
    asyncio.run(main())
