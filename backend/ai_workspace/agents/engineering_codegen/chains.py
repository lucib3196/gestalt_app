from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain import hub
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from IPython.display import Image, display
from typing import Literal, List, Any, Optional
from ast import literal_eval
import json
import os

from .example_template import ExampleBasedTemplate



# ─────────────────────────────────────────────────────
# 🔹 Pydantic Models (Schemas)
# ─────────────────────────────────────────────────────

class CodeResponse(BaseModel):
    code: str = Field(..., description="The generate code. Only return the code")

class QuestionMetadata(BaseModel):
    title: str
    question: str
    stem: str
    topic: str
    tags: List[str]
    prereqs: List[str]
    isAdaptive: Literal['True', 'False']

class InitialMetadata(BaseModel):
    createdBy: str
    qtype: str
    nSteps: int
    updatedBy: str
    codelang: str
    reviewed: Literal['True', 'False']
    ai_generated: Literal['True', 'False']

class InputState(BaseModel):
    query: str
    initial_metadata: Optional[InitialMetadata] = None

class OverallState(BaseModel):
    question: str
    question_html: str
    server_js: str
    server_py: str
    solution_html: str
    metadata: dict[str, Any]
    isAdaptive: Literal['True', 'False']
    
    
class FilesData(BaseModel):
    question_txt: str
    question_html:str
    server_js:str
    server_py:str
    solution_html:str
    metadata:str
    
class OutputState(BaseModel):
    title: str
    files_data: FilesData
    

# ───────────────────────────────────────────
# ──────────
# 🔹 LLM Initialization
# ─────────────────────────────────────────────────────

llm = ChatOpenAI(model="gpt-4o")
llm_code_struct = llm.with_structured_output(CodeResponse)

# ─────────────────────────────────────────────────────
# 🔹 Node Functions
# ─────────────────────────────────────────────────────

def analyze_question(state: InputState) -> OverallState:
    prompt = hub.pull("gestalt_metadata")
    chain = prompt | llm.with_structured_output(QuestionMetadata)
    response = chain.invoke({"question": state.query})
    response = json.loads(response.model_dump_json())

    metadata = {
        **state.initial_metadata.model_dump(),
        **response
    }

    return {
        "question": response.get("question"),
        "metadata": metadata,
        "isAdaptive": response.get("isAdaptive", "True")
    }

def generate_html(state: OverallState) -> OverallState:
    base_prompt = hub.pull("question_html_template")
    prompt = ExampleBasedTemplate(
        column_names=["question", "question.html"],
        base_template=base_prompt,
        filter={"isAdaptive": state.isAdaptive}
    ).generate_prompt(query=state.question)

    response = llm_code_struct.invoke([prompt]).model_dump()

    return {
        'question': state.question,
        'isAdaptive': state.isAdaptive,
        'question_html': response.get("code", ""),
        'server_js': '',
        'server_py': '',
        'solution_html': ''
    }

def generate_js(state: OverallState) -> dict:
    base_prompt = hub.pull("server_js_template_base")
    prompt = ExampleBasedTemplate(
        column_names=["question.html", "server.js"],
        base_template=base_prompt
    ).generate_prompt(query=state.question_html)

    return {'server_js': llm_code_struct.invoke([prompt]).model_dump().get("code", "")}

def generate_py(state: OverallState) -> dict:
    base_prompt = hub.pull("server_py_template_base1")
    prompt = ExampleBasedTemplate(
        column_names=["question.html", "server.py"],
        base_template=base_prompt
    ).generate_prompt(query=state.question_html)

    return {'server_py': llm_code_struct.invoke([prompt]).model_dump().get("code", "")}

def generate_solution_html(state: OverallState) -> dict:
    base_prompt = hub.pull("solution_html_template")
    prompt = ExampleBasedTemplate(
        column_names=["question.html", "solution.html"],
        base_template=base_prompt,
        filter={"isAdaptive": state.isAdaptive}
    ).generate_prompt(query=state.question_html)

    return {'solution_html': llm_code_struct.invoke([prompt]).model_dump().get("code", "")}

def is_adaptive_router(state: OverallState):
    return ['generate_js', 'generate_py'] if literal_eval(state.isAdaptive) else []

def combine_(state:OverallState)->OutputState:
    question_text = f"The original question was {state.question}"
    title = state.metadata.get("title", "untitled")
    metadata  = json.dumps(state.metadata)
    files_data = {
    "question_txt": question_text,
    "question_html": state.question_html,
    "server_js": state.server_js,
    "server_py": state.server_py,
    "solution_html": state.solution_html,
    "metadata": metadata}
    
    files_data = FilesData(**files_data)
    return {"title": title, "files_data": files_data}

# ─────────────────────────────────────────────────────
# 🔹 LangGraph Build
# ─────────────────────────────────────────────────────

graph_builder = StateGraph(
    OverallState,
    input=InputState,
    output=OutputState,
    config_schema=InitialMetadata
)

graph_builder.add_node('analyze_question_genmeta', analyze_question)
graph_builder.add_node('generate_html', generate_html)
graph_builder.add_node('generate_js', generate_js)
graph_builder.add_node('generate_py', generate_py)
graph_builder.add_node('generate_solution_html', generate_solution_html)
graph_builder.add_node('combine_',combine_)

graph_builder.add_edge(START, 'analyze_question_genmeta')
graph_builder.add_edge('analyze_question_genmeta', 'generate_html')
graph_builder.add_edge('generate_html', 'generate_solution_html')
graph_builder.add_edge('generate_solution_html', 'combine_')
graph_builder.add_edge('generate_js', 'combine_')
graph_builder.add_edge('generate_py', 'combine_')
graph_builder.add_edge('combine_', END)

graph_builder.add_conditional_edges('generate_html', is_adaptive_router, ['generate_js', 'generate_py'])

# Compile
graph = graph_builder.compile()

# ─────────────────────────────────────────────────────
# 🔹 Visualization Utility
# ─────────────────────────────────────────────────────

def save_graph_image(graph, filename="Generate_QuestionGraph.png"):
    try:
        image = graph.get_graph().draw_mermaid_png()
        display(Image(image))

        with open(os.path.join(os.path.dirname(__file__), filename), 'wb') as f:
            f.write(image)
            print(f"Saved Image at {filename}")

    except Exception as e:
        print(f"Graph visualization failed: {e}")

# ─────────────────────────────────────────────────────
# 🔹 Execute for Testing
# ─────────────────────────────────────────────────────

if __name__ == "__main__":
    metadata_dict = {
        "createdBy": "lberm007@ucr.edu",
        "qtype": "num",
        "nSteps": 1,
        "updatedBy": "",
        "difficulty": 1,
        "codelang": "javascript",
        "reviewed": "False",
        "ai_generated": "True"
    }
    initial_metadata = InitialMetadata(**metadata_dict)

    # Example 1
    question_1 = r"""
    **Question:**  
    A car accelerates from rest at a constant rate of \( 3 \, \text{m/s}^2 \). How far does it travel in 5 seconds?

    **Follow-up:**  
    What is its final velocity at the end of the 5 seconds?
    """
    save_graph_image(graph)
    result = graph.invoke({'query': question_1, "initial_metadata": initial_metadata})
    print(result)
    print("*" * 60)

    # Example 2
    question_2 = """Question:
    Which of the following best describes Newton's First Law of Motion?

    Choices:
    A. Force equals mass times acceleration
    B. Every action has an equal and opposite reaction
    C. An object in motion stays in motion unless acted on by an external force
    D. Energy cannot be created or destroyed

    Answer:
    C. An object in motion stays in motion unless acted on by an external force
    """
    result = graph.invoke({'query': question_2, "initial_metadata": initial_metadata})
    print(result) 
    import asyncio
    async def main():
        question_list = [question_1, question_2]
        # Create a list of asynchronous tasks
        tasks = [graph.abatch({'query': query, 'initial_metadata': initial_metadata})
                for query in question_list]
        # Await on asyncio.gather so that all tasks run concurrently.
        results = await asyncio.gather(*tasks)
        print(results)
    asyncio.run(main())