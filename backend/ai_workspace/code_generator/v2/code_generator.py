import os
import asyncio
from ast import literal_eval
from typing import Any, List, Optional, Annotated
import operator
import json
from pydantic import BaseModel, Field
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy

from ...agents.engineering_codegen.example_template import ExampleBasedTemplate
from ...models.questionModels import (
    InitialMetadata,
    QuestionMetadata,
    CodeResponse,
    FilesData,
    Question,
)
from ...models.tokenCounter import TokenUsage, StepTokenUsage
from ...utils.helper import (
    save_graph_visualization,
    to_serializable,
    extract_token_usage,
    parse_structured,
)
from ...utils.reducers import merge_files_data, keep_first, reduce_token_usage


# Constants
FAST_LLM = "gpt-4o-mini"
LONG_CONTEXT = "gpt-4o"

# LLM clients
fast_llm = ChatOpenAI(model=FAST_LLM)
long_context_llm = ChatOpenAI(model=FAST_LLM)


# State Models
class CodeGenInput(BaseModel):
    question_payload: Question
    question_metadata: Optional[InitialMetadata] = Field(
        None, title="Initial Metadata from the user"
    )


class CodeGenState(BaseModel):
    question_payload: Annotated[Question, keep_first]
    question_metadata: Annotated[Optional[QuestionMetadata], keep_first] = Field(
        ..., title="Initial Metadata from the user"
    )
    files: Annotated[FilesData, merge_files_data] = Field(default_factory=FilesData)
    token_usage: Annotated[List[StepTokenUsage], reduce_token_usage] = Field(
        default_factory=list
    )
    isAdaptive: Annotated[bool, keep_first]


# Graph Nodes
async def classify_question(state: CodeGenInput) -> CodeGenState:
    metadata_prompt = hub.pull("gestalt_metadata")
    chain = metadata_prompt | fast_llm.with_structured_output(
        QuestionMetadata, include_raw=True
    )
    result = await chain.ainvoke({"question": state.question_payload.question})
    ai_message = result["raw"]
    question_metadata = parse_structured(QuestionMetadata, ai_message)
    token_step = extract_token_usage(ai_message, "classify_question")
    return {
        "question_metadata": question_metadata,
        "isAdaptive": question_metadata.isAdaptive,
        "token_usage": [token_step],
    }


async def generate_question_html(state: CodeGenState) -> CodeGenState:
    base_prompt = hub.pull("question_html_template")
    template = ExampleBasedTemplate(
        column_names=["question", "question.html"],
        base_template=base_prompt,
        filter={"isAdaptive": state.isAdaptive},
    )
    prompt_text = template.generate_prompt(query=state.question_payload.question)
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    result = await chain.ainvoke([prompt_text])
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    token_step = extract_token_usage(ai_message, "generate_question_html")
    state.files.question_html = structured.code
    state.token_usage.append(token_step)
    return state


async def generate_server_js(state: CodeGenState) -> CodeGenState:
    base_prompt = hub.pull("server_js_template_base")
    template = ExampleBasedTemplate(
        column_names=["question.html", "server.js"],
        base_template=base_prompt,
        filter={"isAdaptive": state.isAdaptive},
    )
    prompt_text = template.generate_prompt(query=state.question_payload.question, k=1)
    if state.question_payload.solution_as_str:
        prompt_text += f"\nSolution Guide: {state.question_payload.solution_as_str}\nUse this guide to aid in the creation of the code by following its logic."
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    result = await chain.ainvoke([prompt_text])
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    token_step = extract_token_usage(ai_message, "generate_server_js")
    state.files.server_js = structured.code
    state.token_usage.append(token_step)
    return state


async def generate_server_py(state: CodeGenState) -> CodeGenState:
    base_prompt = hub.pull("server_py_template_base1")
    template = ExampleBasedTemplate(
        column_names=["question.html", "server.py"],
        base_template=base_prompt,
        filter={"isAdaptive": state.isAdaptive},
    )
    prompt_text = template.generate_prompt(query=state.question_payload.question, k=1)
    if state.question_payload.solution_as_str:
        prompt_text += f"\nSolution Guide: {state.question_payload.solution_as_str}\nUse this guide to aid in the creation of the code by following its logic."
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    result = await chain.ainvoke([prompt_text])
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    token_step = extract_token_usage(ai_message, "generate_server_py")
    state.files.server_py = structured.code
    state.token_usage.append(token_step)
    return state


async def generate_solution_html(state: CodeGenState) -> CodeGenState:
    base_prompt = hub.pull("question_html_template")
    template = ExampleBasedTemplate(
        column_names=["question.html", "server.py"],
        base_template=base_prompt,
        filter={"isAdaptive": state.isAdaptive},
    )
    prompt_text = template.generate_prompt(query=state.question_payload.question, k=1)
    if state.question_payload.solution_as_str:
        prompt_text += f"\nSolution Guide: {state.question_payload.solution_as_str}\nUse this guide to aid in the creation of the code by following its logic."
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    result = await chain.ainvoke([prompt_text])
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    token_step = extract_token_usage(ai_message, "generate_solution_html")
    state.files.solution_html = structured.code
    state.token_usage.append(token_step)
    return state


def conditional_js_py_router(state: CodeGenState) -> List[str]:
    return (
        ["generate_server_js", "generate_server_py"]
        if literal_eval(state.isAdaptive)
        else []
    )


def solution_improvement_router(state: CodeGenState) -> str:
    is_adaptive = state.question_metadata.isAdaptive
    if isinstance(is_adaptive, str):
        is_adaptive = literal_eval(is_adaptive)
    return "adaptive_combine" if is_adaptive else "final_combine"


async def adaptive_combine(state: CodeGenState) -> CodeGenState:
    improve_prompt = ChatPromptTemplate.from_template(
        """
        You are tasked with analyzing the following solution guide and its corresponding code...
        ---
        Solution HTML:
        {solution_guide}
        ---
        Code:
        {code}
        ---
        Return the improved solution HTML.
        """
    )
    chain = improve_prompt | fast_llm.with_structured_output(
        CodeResponse, include_raw=True
    )
    result = await chain.ainvoke(
        {"solution_guide": state.files.solution_html, "code": state.files.server_js}
    )
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    token_step = extract_token_usage(ai_message, "adaptive_combine")
    state.files.solution_html = structured.code
    state.token_usage.append(token_step)
    return state


async def final_combine(state: CodeGenState) -> CodeGenState:
    metadata = {}
    if state.question_metadata:
        metadata.update(state.question_metadata.model_dump())
    if state.files.metadata:
        metadata.update(state.files.metadata)
    state.files.metadata = metadata
    return state


# Build and compile graph
graph = StateGraph(CodeGenState, input=CodeGenInput)

nodes = [
    ("classify_question", classify_question),
    ("generate_question_html", generate_question_html),
    ("generate_server_js", generate_server_js),
    ("generate_server_py", generate_server_py),
    ("generate_solution_html", generate_solution_html),
    ("adaptive_combine", adaptive_combine),
    ("final_combine", final_combine),
]
for name, func in nodes:
    graph.add_node(name, func, retry=RetryPolicy(max_attempts=1))

graph.add_edge(START, "classify_question")
graph.add_edge("classify_question", "generate_question_html")
graph.add_edge("generate_question_html", "generate_solution_html")
graph.add_conditional_edges(
    "generate_question_html",
    conditional_js_py_router,
    ["generate_server_js", "generate_server_py"],
)
graph.add_edge("generate_server_js", "adaptive_combine")
graph.add_edge("generate_server_py", "adaptive_combine")
graph.add_conditional_edges(
    "generate_solution_html",
    solution_improvement_router,
    ["adaptive_combine", "final_combine"],
)
graph.add_edge("adaptive_combine", "final_combine")
graph.add_edge("final_combine", END)

compiled_graph = graph.compile()


async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    save_graph_visualization(
        compiled_graph,
        filename="CodeGeneratorV2.png",
        base_path=base_path,
    )
    question = "A car is traveling along a straight road at 60 mph; calculate distance after 4 hours"
    input_state = CodeGenInput(question_payload=Question(question=question))
    result = await compiled_graph.ainvoke(input_state)
    with open(os.path.join(base_path, "codeGeneratorv2.json"), "w") as f:
        json.dump(to_serializable(result), f, indent=4, default=str)


if __name__ == "__main__":
    asyncio.run(main())
