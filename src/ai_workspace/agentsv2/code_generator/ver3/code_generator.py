from typing import Optional, Annotated, List, Dict, Literal
from pydantic import BaseModel, Field
from ai_workspace.utils import save_graph_visualization, keep_first, merge_files_data
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.pregel import RetryPolicy  # type: ignore
from langchain_core.prompts import ChatPromptTemplate
import operator

from schemas import Question, InitialMetadata, FilesData
from .question_html import app as question_html_chain, State as QHtmlState
from .server_files import app as js_chain, app_py as py_chain, State as ServerStateInput
from .metadata import compiled_graph as metadata_chain, MetadataState, MetadataInput
from .solution_html import app as solution_chain, State as SolutionInputState

# ────────────────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────────────────
FASTLLM = "gpt-4o-mini"
LONGCONTEXTLLM = "o3-mini-2025-01-31"

fast_llm = ChatOpenAI(model=FASTLLM)
long_context = ChatOpenAI(model=LONGCONTEXTLLM)

MAX_ITERATIONS = 6
# ────────────────────────────────────────────────────────────────────────────────
# Chains
# ────────────────────────────────────────────────────────────────────────────────

# Code fix
code_grader_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert developer tasked with modifying the following code and improving on it.",
        ),
        ("human", "Code: {code}\nChanges to fix:{approach}\n"),
    ]
)


class CodeOutput(BaseModel):
    code: str = Field(..., description="Return just the code")


code_fix_llm = fast_llm.with_structured_output(CodeOutput)
code_fix = code_grader_prompt | code_fix_llm

# Grader prompt
code_grader_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a coding assistant with expertise in creating educational content for engineering/physics/science students. Your primary task is to analyze whether the solution guide, the frontend question display, and the server files (in Python or JavaScript) are fully compatible with one another, especially regarding dynamic placeholders delimited as {{params.value}} or {{correct_answers.value}}. These placeholders must be generated dynamically by the server files and referenced correctly in both the question view and the solution.

Focus on these aspects:
- Ensure all dynamic placeholders in the question and solution are defined and populated by the server files.
- Check that all required imports and variables are present and correctly referenced.
- Identify and implement any necessary unit conversions for physics/math/engineering problems to ensure the solution is accurate and comprehensible. Provide clear instructions on how to perform these conversions in the solution and server files.
- Suggest modifications to the solution guide or server files to make the solution as dynamic and instructive as possible, including showing intermediate steps of computation and conversion to aid student understanding.
- If necessary, recommend changes to the question view, solution, or server files to improve compatibility and educational value.

Your approach should be as specific as possible, detailing what needs to be implemented with clear steps outlining the issues identified and how you plan to address them.

If you need to modify any of the files, return the name of the file you want to modify. Currently, you can modify 'question_html', 'server_js', 'server_py', or 'solution_html'.

Structure your answer as follows:
1. Description of the code solution and its dynamic aspects.
2. List of imports and variables required for compatibility.
3. The functioning code block(s) with any suggested improvements for dynamic content, intermediate steps, and conversions.""",
        ),
        ("human", "{input}"),
    ]
)


class IndividualFileReview(BaseModel):
    file_name: str
    approach: str


class CodeReview(BaseModel):
    analysis: str = Field(
        ...,
        description="An analysis of the code and wether it aligns with the goals given",
    )
    grade: Literal["yes", "no"] = Field(
        ...,
        description="A binary yes or no on wether further modification are needed to improve this code",
    )
    approach: str = Field(
        ..., description="The approach of what needs to be modified in the code"
    )
    files_to_modify: List[IndividualFileReview] = Field(
        ..., description="The name of the files you want to modify and the approach"
    )


code_review = code_grader_prompt | long_context.with_structured_output(CodeReview)
# ────────────────────────────────────────────────────────────────────────────────
# State Models
# ────────────────────────────────────────────────────────────────────────────────


class CodeGenInput(BaseModel):
    """
    Input state for the code generation pipeline.
    """

    question_payload: Annotated[Question, keep_first] = Field(
        ..., description="The question to be processed."
    )
    initial_metadata: Annotated[Optional[InitialMetadata], keep_first] = Field(
        None, description="Metadata about who is running the generators."
    )


class CodeGenState(BaseModel):
    """
    State model representing the current state in the code generation pipeline.
    """

    question_payload: Annotated[Question, keep_first] = Field(
        ..., description="The question to be processed."
    )
    initial_metadata: Annotated[Optional[InitialMetadata], keep_first] = Field(
        None, description="Metadata about who is running the generators."
    )
    question_metadata: Annotated[MetadataState, keep_first] = Field(
        Field(default_factory=MetadataState),
        description="Metadata related to the question.",
    )
    files: Annotated[FilesData | Dict[str, str], merge_files_data] = Field(
        default_factory=FilesData, description="The files to be generated."
    )
    is_adaptive: Annotated[bool, keep_first] = Field(
        default=False, description="Flag indicating if the question is adaptive."
    )
    code_review_message: Annotated[List[CodeReview], operator.add] = Field(
        default_factory=list, description="Code Review Messages"
    )
    iterations: int = Field(0, description="Number of iterations so far.")


# ────────────────────────────────────────────────────────────────────────────────
# Node Functions
# ────────────────────────────────────────────────────────────────────────────────


def extract_question_metadata(state: CodeGenInput) -> CodeGenState:
    """
    Extracts metadata for the question using the metadata_chain.
    """
    metadata_input = MetadataInput(
        question=state.question_payload.question, initial_metadata=None
    )
    result = metadata_chain.invoke(metadata_input)
    return {
        "question_metadata": result,
        "is_adaptive": result.get("isAdaptive"),
    }  # type: ignore


def generate_question_html(state: CodeGenState) -> CodeGenState:
    """
    Generates the HTML representation of the question.
    """
    html_input = QHtmlState(
        question=state.question_payload.question, isAdaptive=state.is_adaptive
    )
    result = question_html_chain.invoke(html_input)
    updated_files = FilesData(question_html=result.get("qfile", ""))
    return {"files": updated_files.model_dump()}  # type: ignore


def route_server_file_generation(state: CodeGenState) -> List[str]:
    """
    Determines which server files (JS/PY) to generate based on adaptivity.
    """
    return (
        ["generate_server_js", "generate_server_py"] if bool(state.is_adaptive) else []
    )


def route_solution_generation(state: CodeGenState) -> str:
    """
    Determines the next step after generating solution HTML.
    """
    return "adaptive_code_review" if bool(state.is_adaptive) else END


def generate_server_js_file(state: CodeGenState) -> CodeGenState:
    """
    Generates the server-side JavaScript file.
    """
    question_html = extract_question_html(state.files)
    js_input = ServerStateInput(
        question_html=question_html,
        solution_guide=state.question_payload.solution_as_str,
        isAdaptive=state.is_adaptive,
    )
    result = js_chain.invoke(js_input)
    updated_files = FilesData(server_js=result.get("server_file", ""))
    return {"files": updated_files.model_dump()}  # type: ignore


def generate_server_py_file(state: CodeGenState) -> CodeGenState:
    """
    Generates the server-side Python file.
    """
    question_html = extract_question_html(state.files)
    py_input = ServerStateInput(
        question_html=question_html,
        solution_guide=state.question_payload.solution_as_str,
        isAdaptive=state.is_adaptive,
    )
    result = py_chain.invoke(py_input)
    updated_files = FilesData(server_py=result.get("server_file", ""))
    return {"files": updated_files.model_dump()}  # type: ignore


def generate_solution_html_file(state: CodeGenState) -> CodeGenState:
    """
    Generates the HTML for the solution.
    """
    question_html = extract_question_html(state.files)
    solution_input = SolutionInputState(
        question=question_html,
        solution=state.question_payload.solution_as_str,
        isAdaptive=state.is_adaptive,
    )
    result = solution_chain.invoke(solution_input)
    updated_files = FilesData(solution_html=result.get("qfile", ""))
    return {"files": updated_files.model_dump()}  # type: ignore


def adaptive_code_review(state: CodeGenState) -> CodeGenState:
    """
    Combines outputs for adaptive questions.
    """

    code_blocks = f"""
    The following is the code to review
    question.html: {state.files.question_html} \n
    solution.html: {state.files.solution_html} \n
    server.js: {state.files.server_js} \n
    server.py {state.files.server_py} \n
    """

    result = code_review.invoke({"input": code_blocks})
    iterations = state.iterations + 1
    return {"code_review_message": [result], "iterations": iterations}  # type: ignore


def decide_to_modify(state: CodeGenState) -> str:
    if state.code_review_message[-1].grade == "yes" and state.iterations < MAX_ITERATIONS:  # type: ignore
        return "modify_code"
    else:
        return END


def decied_to_review(state: CodeGenState):
    if state.iterations < MAX_ITERATIONS:
        return "adaptive_code_review"
    else:
        return END


def modify_code(state: CodeGenState) -> CodeGenState:
    """
    Applies code modifications based on the latest code review feedback.
    """
    last_review = state.code_review_message[-1].files_to_modify
    all_files = state.files.model_dump()  # type: ignore

    for file_mod in last_review:
        filename = file_mod.file_name
        approach = file_mod.approach
        original_code = all_files.get(filename, "")

        # Skip modification if no approach or original code is empty
        if not approach or not original_code:
            continue

        result = code_fix.invoke({"approach": approach, "code": original_code})
        # Only update if code was actually returned
        updated_code = result.code  # type: ignore
        all_files[filename] = updated_code

    return {"files": all_files}  # type: ignore


# ────────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ────────────────────────────────────────────────────────────────────────────────


def extract_question_html(files: Optional[FilesData | Dict[str, str]]) -> str:
    """
    Helper to extract question_html from files.
    """
    if files is not None:
        if isinstance(files, dict):
            return files.get("question_html", "")
        return getattr(files, "question_html", "")
    return ""


# ────────────────────────────────────────────────────────────────────────────────
# Graph Construction
# ────────────────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────────────────
# Graph Construction
# ────────────────────────────────────────────────────────────────────────────────

graph = StateGraph(CodeGenState, input=CodeGenInput)

# Register nodes
graph.add_node(
    "extract_question_metadata",
    extract_question_metadata,
    retry=RetryPolicy(max_attempts=1),
)
graph.add_node(
    "generate_question_html", generate_question_html, retry=RetryPolicy(max_attempts=1)
)
graph.add_node(
    "generate_server_js", generate_server_js_file, retry=RetryPolicy(max_attempts=1)
)
graph.add_node(
    "generate_server_py", generate_server_py_file, retry=RetryPolicy(max_attempts=1)
)
graph.add_node(
    "generate_solution_html",
    generate_solution_html_file,
    retry=RetryPolicy(max_attempts=1),
)
graph.add_node(
    "adaptive_code_review", adaptive_code_review, retry=RetryPolicy(max_attempts=1)
)
graph.add_node("modify_code", modify_code, retry=RetryPolicy(max_attempts=1))

# Register edges
graph.add_edge(START, "extract_question_metadata")
graph.add_edge("extract_question_metadata", "generate_question_html")
graph.add_edge("generate_question_html", "generate_solution_html")

# Conditional: generate server files if adaptive
graph.add_conditional_edges(
    "generate_question_html",
    route_server_file_generation,  # type: ignore
    ["generate_server_js", "generate_server_py"],
)

# Server file generation leads to code review
graph.add_edge("generate_server_js", "adaptive_code_review")
graph.add_edge("generate_server_py", "adaptive_code_review")

# Conditional: after solution HTML, either combine outputs or end
graph.add_conditional_edges(
    "generate_solution_html",
    route_solution_generation,
    ["adaptive_code_review", END],
)

# Code review can lead to modification or end
graph.add_conditional_edges(
    "adaptive_code_review",
    decide_to_modify,
    ["modify_code", END],
)
graph.add_conditional_edges(
    "modify_code",
    decied_to_review,
    ["adaptive_code_review", END],
)


# If code is modified, process ends (can be extended for further iterations)
graph.add_edge("adaptive_code_review", END)
compiled_graph = graph.compile()


# ────────────────────────────────────────────────────────────────────────────────
# Main Entrypoint
# ────────────────────────────────────────────────────────────────────────────────
def main():
    """
    Main function to visualize and run the code generation pipeline.
    """
    save_graph_visualization(
        compiled_graph,  # type: ignore
        filename="CodeGeneratorV3.png",
        base_path=r"ai_workspace/agentsv2/code_generator/ver3/graphs",
    )
    question = "A car is traveling along a straight road at 60 mph; calculate distance after 4 hours"
    input_state = CodeGenInput(
        question_payload=Question(question=question),  # type: ignore
        initial_metadata=None,
    )  # type: ignore
    for chunk in compiled_graph.stream(input_state, stream_mode="updates"):
        print(chunk)


if __name__ == "__main__":
    main()
