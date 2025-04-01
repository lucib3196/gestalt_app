from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel,Field
from IPython.display import Image, display
import os
from typing import Literal
import json
from ast import literal_eval
from .example_template import ExampleBasedTemplate
from langchain import hub

# ---------- Initialize LLM ---------- #

llm = ChatOpenAI(model="gpt-4o")

# --- Define Structure Output Schemas
class CodeResponse(BaseModel):
    code: str = Field(..., description="The generate code. Only return the code")
    
# For now assume that we are only returning the code
llm_code_struct = llm.with_structured_output(CodeResponse)

# ---------- Define States ---------- #

class InputState(BaseModel):
    query: str


class QuestionInfo(BaseModel):
    question: str
    isAdaptive: Literal['True', 'False']


class OverallState(BaseModel):
    question: str
    question_html: str
    server_js: str
    server_py: str
    solution_html: str
    isAdaptive: Literal['True', 'False']


# ---------- Node Functions ---------- #

def analyze_question(state: InputState) -> QuestionInfo:
    prompt = f"""
    Analyze the following input. If it's a computational question, set `isAdaptive` to "True".
    Otherwise, set it to "False" (e.g., multiple choice or conceptual questions).
    Also return the cleaned-up version of the question.

    Input:
    {state.query}
    """
    llm_struc = llm.with_structured_output(QuestionInfo)
    response = llm_struc.invoke([prompt])
    return json.loads(response.model_dump_json())


def generate_html(state: QuestionInfo) -> OverallState:
    filter_ = {'isAdaptive': state.isAdaptive}
    base_prompt=hub.pull("question_html_template"),
    prompt = ExampleBasedTemplate(
        column_names=["question", "question.html"],
        base_template=base_prompt,
        filter=filter_
    ).generate_prompt(query=state.question)
    
    response = llm_code_struct.invoke([prompt])
    response = response.dict()
    
    return {
        'question': state.question,
        'isAdaptive': state.isAdaptive,
        'question_html': response.get("code",""),
        'server_js': '',
        'server_py': '',
        'solution_html': ''
    }


def generate_js(state: OverallState) -> dict:
    base_prompt=hub.pull("server_js_template_base")
    prompt = ExampleBasedTemplate(
        column_names=["question.html", "server.js"],
        base_template=base_prompt
    ).generate_prompt(query=state.question_html)
    
    response = llm_code_struct.invoke([prompt])
    response = response.dict()
    return {'server_js':  response.get("code","")}


def generate_py(state: OverallState) -> dict:
    
    base_prompt=hub.pull("server_py_template_base1"),
    prompt = ExampleBasedTemplate(
        column_names=["question.html", "server.py"],
        base_template=base_prompt
    ).generate_prompt(query=state.question_html)
    
    response = llm_code_struct.invoke([prompt])
    response = response.dict()
    return {'server_py': response.get("code","")}


def generate_solution_html(state: OverallState) -> dict:
    filter = {'isAdaptive': state.isAdaptive}
    base_prompt=hub.pull("solution_html_template"),
    prompt = ExampleBasedTemplate(
        column_names=["question.html", "solution.html"],
        base_template=base_prompt,
        filter=filter
    ).generate_prompt(query=state.question_html)
    
    response = llm_code_struct.invoke([prompt])
    response = response.dict()
    
    return {'solution_html':response.get("code","")}


def is_adaptive_router(state: OverallState):
    is_adaptive = literal_eval(state.isAdaptive)
    
    if is_adaptive:
        print('Question is Adaptive → Routing to JS and PY generators')
        return ['generate_js', 'generate_py']
    
    print('Question is Non-Adaptive → Skipping generators')
    return []


# ---------- Build LangGraph ---------- #

graph_builder = StateGraph(OverallState, input=InputState, output=OverallState)

# Add nodes
graph_builder.add_node('analyze_question', analyze_question)
graph_builder.add_node('generate_html', generate_html)
graph_builder.add_node('generate_js', generate_js)
graph_builder.add_node('generate_py', generate_py)
graph_builder.add_node('generate_solution_html', generate_solution_html)

# Add edges
graph_builder.add_edge(START, 'analyze_question')
graph_builder.add_edge('analyze_question', 'generate_html')

graph_builder.add_conditional_edges(
    'generate_html',
    is_adaptive_router,
    ['generate_js', 'generate_py']
)

graph_builder.add_edge('generate_html', 'generate_solution_html')
graph_builder.add_edge('generate_js', END)
graph_builder.add_edge('generate_py', END)
graph_builder.add_edge('generate_solution_html', END)

graph = graph_builder.compile()


# ---------- Visualization Helper ---------- #

def save_graph_image(graph, filename="Generate_QuestionGraph.png"):
    try:
        image = graph.get_graph().draw_mermaid_png()
        display(Image(image))
        
        with open(os.path.join(os.path.dirname(__file__), filename), 'wb') as f:
            f.write(image)
            print(f"Saved Image at {filename}")
    
    except Exception as e:
        print(f"Graph visualization failed: {e}")

if __name__ == "__main__":
    sample_question = r"""
    **Question:**  
    A car accelerates from rest at a constant rate of \( 3 \, \text{m/s}^2 \). How far does it travel in 5 seconds?

    **Follow-up:**  
    What is its final velocity at the end of the 5 seconds?
    """
    save_graph_image(graph)
    result = graph.invoke({'query': sample_question})
    print(result)
    print(f'{'*'*60}\n\n\n')
    sample_question = """Question:
        Which of the following best describes Newton's First Law of Motion?

        Choices:
        A. Force equals mass times acceleration
        B. Every action has an equal and opposite reaction
        C. An object in motion stays in motion unless acted on by an external force
        D. Energy cannot be created or destroyed

        Answer:
        C. An object in motion stays in motion unless acted on by an external force
        """
    result = graph.invoke({'query': sample_question})
    print(result)
