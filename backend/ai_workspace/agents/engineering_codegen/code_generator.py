# =============================================================================
# Standard Library Imports
# =============================================================================
import json
import os
from ast import literal_eval
from typing import Any, List, Literal, Optional, TypedDict, Annotated
import operator

# =============================================================================
# Third-Party Imports
# =============================================================================
from IPython.display import Image, display
from pydantic import BaseModel, Field

# =============================================================================
# LangChain & LangGraph Imports
# =============================================================================
from langchain import hub
from langchain_core.runnables import RunnableConfig, chain as as_runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy

# =============================================================================
# Local Package Imports
# =============================================================================
from .example_template import ExampleBasedTemplate
from .question_metadata_graph import (
    QuestionPayload,
    QuestionMetadata,
    QuestionBuildState,
    analyze_question_and_genmetadata,
)

# =============================================================================
# Reducer Functions
# =============================================================================
def keep_first(existing: Any, new: Any) -> Any:
    """
    Reducer function that returns the first (existing) value if available.
    """
    return existing or new


def merge_files_data(existing: "FilesData", new: "FilesData") -> "FilesData":
    """
    Merges two FilesData instances by taking non-empty fields from the new value.
    """
    return FilesData(
        question_html=new.question_html or existing.question_html,
        server_js=new.server_js or existing.server_js,
        server_py=new.server_py or existing.server_py,
        solution_html=new.solution_html or existing.solution_html,
        metadata=new.metadata or existing.metadata,
    )


# =============================================================================
# LLM Definitions
# =============================================================================
# Fast LLM: for shorter tasks or rapid responses.
fast_llm = ChatOpenAI(model="gpt-4o-mini")
# Long Context LLM: for inputs that require higher levels of reasoning.
long_context_llm = ChatOpenAI(model="gpt-4o")


# =============================================================================
# Pydantic Models
# =============================================================================
class FilesData(BaseModel):
    """Holds the generated file contents related to a question."""

    question_html: str = ""
    server_js: str = ""
    server_py: str = ""
    solution_html: str = ""
    metadata: dict[str,Any] = {}

class InitialMetadata(BaseModel):
    createdBy: str
    qtype:str
    nSteps: int
    updatedBy:str
    codelang:str
    reviewed: Literal["True", "False"]
    ai_generated: Literal["True","False"]

class QuestionPackage(BaseModel):
    """
    Overall package containing the question payload, metadata, and generated files.
    
    The fields are annotated with reducer functions to merge concurrent updates.
    """
    question_payload: Annotated[QuestionPayload, keep_first]
    question_metadata: Annotated[Optional[QuestionMetadata], keep_first] = None
    files: Annotated[FilesData, merge_files_data] = Field(default_factory=FilesData)
    initial_metadata: Annotated[Optional[InitialMetadata], keep_first] = None

class CodeResponse(BaseModel):
    """Output schema from the LLM for code generation."""
    code: str = Field(..., description="The generated code. Only return the code.")

# =============================================================================
# Runnable Nodes (Chain Functions)
# =============================================================================
@as_runnable
async def analyze_question_and_generate_metadata(question: str) -> QuestionMetadata:
    """
    Analyzes a question string and generates metadata.
    
    Utilizes a prompt pulled via hub and returns structured output.
    """
    metadata_prompt = hub.pull("gestalt_metadata")
    metadata_chain = metadata_prompt | fast_llm.with_structured_output(QuestionMetadata)
    return await metadata_chain.ainvoke({"question": question})


async def generate_metadata(state: QuestionPackage) -> QuestionPackage:
    """
    Generates metadata for the input question and updates the state.
    
    Args:
        state: A QuestionPackage instance containing the question payload.
        
    Returns:
        Updated state with question metadata populated.
    """
    question_text = state.question_payload.question
    metadata = await analyze_question_and_generate_metadata.ainvoke({"question": question_text})
    state.question_metadata = metadata
    return state


async def generate_html(state: QuestionPackage) -> QuestionPackage:
    """
    Generates the HTML content for the question using a prompt template.
    
    The generated HTML is stored in the files.question_html field.
    
    Args:
        state: A QuestionPackage instance.
        
    Returns:
        Updated state with HTML content generated.
    """
    base_html_prompt = hub.pull("question_html_template")
    question_text = state.question_payload.question
    is_adaptive = state.question_metadata.isAdaptive

    prompt_text = ExampleBasedTemplate(
        column_names=["question", "question.html"],
        base_template=base_html_prompt,
        filter={"isAdaptive": is_adaptive},
    ).generate_prompt(query=question_text)

    chain = fast_llm.with_structured_output(CodeResponse)
    response = await chain.ainvoke([prompt_text])
    result = response.model_dump()
    generated_html = result.get("code", "")
    state.files.question_html = generated_html
    return state


async def generate_js(state: QuestionPackage) -> QuestionPackage:
    """
    Generates JavaScript code based on the generated HTML and additional inputs.
    
    Updates the files.server_js field in the state.
    
    Args:
        state: A QuestionPackage instance.
        
    Returns:
        Updated state with generated JavaScript code.
    """
    base_js_prompt = hub.pull("server_js_template_base")
    html_content = state.files.question_html
    solution_guide = state.question_payload.solution_guide
    additional_instructions = state.question_payload.additional_instructions

    prompt_text = ExampleBasedTemplate(
        column_names=["question.html", "server.js"],
        base_template=base_js_prompt
    ).generate_prompt(query=html_content, k=1)

    if solution_guide:
        prompt_text += (
            f"\nSolution Guide: {solution_guide}\n"
            "Use this guide to aid in the creation of the code by following its logic."
        )
    if additional_instructions:
        prompt_text += (
            f"\nAdditional Instructions: {additional_instructions}\n"
            "Analyze these and implement if possible."
        )

    chain = long_context_llm.with_structured_output(CodeResponse)
    response = await chain.ainvoke([prompt_text])
    result = response.model_dump()
    generated_js = result.get("code", "")
    state.files.server_js = generated_js
    return state


async def generate_py(state: QuestionPackage) -> QuestionPackage:
    """
    Generates Python code based on the generated HTML and additional inputs.
    
    Updates the files.server_py field in the state.
    
    Args:
        state: A QuestionPackage instance.
        
    Returns:
        Updated state with generated Python code.
    """
    base_py_prompt = hub.pull("server_py_template_base1")
    html_content = state.files.question_html
    solution_guide = state.question_payload.solution_guide
    additional_instructions = state.question_payload.additional_instructions

    prompt_text = ExampleBasedTemplate(
        column_names=["question.html", "server.py"],
        base_template=base_py_prompt
    ).generate_prompt(query=html_content, k=1)

    if solution_guide:
        prompt_text += (
            f"\nSolution Guide: {solution_guide}\n"
            "Use this guide to aid in the creation of the code by following its logic."
        )
    if additional_instructions:
        prompt_text += (
            f"\nAdditional Instructions: {additional_instructions}\n"
            "Analyze these and implement if possible."
        )

    chain = long_context_llm.with_structured_output(CodeResponse)
    response = await chain.ainvoke([prompt_text])
    result = response.model_dump()
    generated_py = result.get("code", "")
    state.files.server_py = generated_py
    return state


async def generate_solution_html(state: QuestionPackage) -> QuestionPackage:
    """
    Generates the final solution HTML using a prompt template along with any additional context.
    
    Updates the files.solution_html field in the state.
    
    Args:
        state: A QuestionPackage instance.
        
    Returns:
        Updated state with the final solution HTML.
    """
    base_solution_prompt = hub.pull("question_html_template")
    html_content = state.files.question_html
    is_adaptive = state.question_metadata.isAdaptive
    solution_guide = state.question_payload.solution_guide
    additional_instructions = state.question_payload.additional_instructions

    prompt_text = ExampleBasedTemplate(
        column_names=["question.html", "solution.html"],
        base_template=base_solution_prompt,
        filter={"isAdaptive": is_adaptive},
    ).generate_prompt(query=html_content)

    if solution_guide:
        prompt_text += (
            f"\nSolution Guide: {solution_guide}\n"
            "Use this guide to aid in the creation of the code by following its logic."
        )
    if additional_instructions:
        prompt_text += (
            f"\nAdditional Instructions: {additional_instructions}\n"
            "Analyze these and implement if possible."
        )

    chain = fast_llm.with_structured_output(CodeResponse)
    response = await chain.ainvoke([prompt_text])
    result = response.model_dump()
    final_solution_html = result.get("code", "")
    state.files.solution_html = final_solution_html
    return state


async def adaptive_combine(state: QuestionPackage) -> QuestionPackage:
    """
    Combines the adaptive solution HTML with the generated server JavaScript code.
    
    Uses a prompt to verify that the solution guide is compatible with the code.
    Updates the files.solution_html field with the improved solution.
    
    Args:
        state: A QuestionPackage instance.
        
    Returns:
        Updated state with the combined solution HTML.
    """
    print("Running Adaptive Combine")
    solution_html = state.files.solution_html
    generated_js = state.files.server_js

    improve_solution_prompt = ChatPromptTemplate.from_template(
        """
        You are tasked with analyzing the following solution guide and its corresponding 
        computational code file. Your goal is to ensure that both are compatible with one another.

        The values generated and exported in the `params` data structure from the code 
        will be dynamically injected into the solution guide. Therefore, it is essential that 
        the variable names, formats, and expected outputs align properly between the code 
        and the solution guide.

        Carefully check for consistency in:
        - Variable names and units
        - Value formatting (e.g., decimal places)
        - Logical flow and correctness of injected data
        - Any discrepancies or missing elements that could break the integration

        ---
        Solution HTML:
        {solution_guide}

        ---
        Code:
        {code}

        ---
        You are tasked with returning the improved solution HTML.
        """
    )

    chain = improve_solution_prompt | fast_llm.with_structured_output(CodeResponse)
    response = await chain.ainvoke({"solution_guide": solution_html, "code": generated_js})
    result = response.model_dump()
    improved_solution_html = result.get("code", "")
    state.files.solution_html = improved_solution_html
    return state


async def final_combine(state: QuestionPackage) -> QuestionPackage:
    """
    Final node to finalize the package.
    
    This node can be used to perform any last steps before ending the graph execution.
    
    Args:
        state: A QuestionPackage instance.
        
    Returns:
        The final state (possibly modified) for the question package.
    """
    print("Finalizing Package")
    state.files.metadata = {**state.question_metadata.model_dump(),
                            **state.initial_metadata.model_dump()}
    return state


# =============================================================================
# Conditional Router Functions
# =============================================================================
def conditional_js_py_router(state: QuestionPackage) -> List[str]:
    """
    Determines whether to route the flow for JavaScript/Python code generation.
    
    Returns a list of node names to execute if the question is adaptive.
    """
    is_adaptive = state.question_metadata.isAdaptive
    return ["generate_js", "generate_py"] if literal_eval(is_adaptive) else []


def solution_improvement_router(state: QuestionPackage) -> str:
    """
    Routes to the adaptive combine node if the question is adaptive;
    otherwise, routes to the end of the graph.
    """
    is_adaptive = state.question_metadata.isAdaptive
    if isinstance(is_adaptive, str):
        is_adaptive = literal_eval(is_adaptive)
    else:
        is_adaptive = bool(is_adaptive)
    return "adaptive_combine" if is_adaptive else END


# =============================================================================
# Graph Construction
# =============================================================================
# Initialize the state graph with the QuestionPackage model.
question_graph = StateGraph(QuestionPackage)

# Define graph nodes as a list of (node_name, function) pairs.
graph_nodes = [
    ("generate_metadata", generate_metadata),
    ("generate_question_html", generate_html),
    ("generate_js", generate_js),
    ("generate_py", generate_py),
    ("generate_solution_html", generate_solution_html),
    ("adaptive_combine", adaptive_combine),
    ("final_combine", final_combine)
]

# Add nodes with retry policy.
for node_name, node_func in graph_nodes:
    question_graph.add_node(node_name, node_func, retry=RetryPolicy(max_attempts=1))

# Construct graph edges.
question_graph.add_edge(START, graph_nodes[0][0])
question_graph.add_edge("generate_metadata", "generate_question_html")
question_graph.add_edge("generate_question_html", "generate_solution_html")

question_graph.add_conditional_edges(
    "generate_question_html", conditional_js_py_router, ["generate_js", "generate_py"]
)
question_graph.add_conditional_edges(
    "generate_solution_html", solution_improvement_router, ["adaptive_combine", "final_combine"]
)
question_graph.add_edge("generate_js", "adaptive_combine")
question_graph.add_edge("generate_py", "adaptive_combine")
question_graph.add_edge("adaptive_combine", "final_combine")
question_graph.add_edge(graph_nodes[-1][0], END)

# Compile the graph.
compiled_graph = question_graph.compile()


# =============================================================================
# Graph Visualization Function (Optional)
# =============================================================================
def save_graph_visualization(graph: StateGraph, filename: str = "CodeBuilder.png") -> None:
    """
    Visualizes the graph and saves it as a PNG image.

    Args:
        graph: The StateGraph instance.
        filename: The filename to save the image.
    """
    try:
        image_bytes = graph.get_graph().draw_mermaid_png()
        display(Image(image_bytes))
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, "wb") as file:
            file.write(image_bytes)
        print(f"Saved graph visualization at {filename}")
    except Exception as error:
        print(f"Graph visualization failed: {error}")


# =============================================================================
# Main Entry Point
# =============================================================================
async def main() -> None:
    """
    Main function to execute the graph starting with an initial state.
    
    An initial question is provided; the graph then processes it,
    generating metadata, HTML, JavaScript, Python, and final solution HTML.
    """
    question_payload = {
        "question": (
            "What is the final velocity of a 2 kg projectile launched at 30 degrees "
            "with an initial speed of 20 m/s after 3 seconds?"
        ),
        "solution_guide": None,
        "additional_instructions": None,
    }
    initial_metadata =  {
        "createdBy": "lberm007@ucr.edu",
        "qtype": "num",
        "nSteps": 1,
        "updatedBy": "",
        "difficulty": 1,
        "codelang": "javascript",
        "reviewed": "False",
        "ai_generated": "True"
    }
    
    graph_input = QuestionPackage(question_payload=question_payload, initial_metadata=initial_metadata)
    result = await compiled_graph.ainvoke(graph_input)
    print(result)


if __name__ == "__main__":
    # Optionally save the graph visualization.
    save_graph_visualization(compiled_graph)
    import asyncio

    asyncio.run(main())
