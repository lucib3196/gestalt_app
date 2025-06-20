from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel
from ai_workspace.utils.helper import save_graph_visualization, parse_structured
from typing import Optional
from ai_workspace.retrievers import SemanticExamplesCSV
from langgraph.graph import END, StateGraph, START
from langchain import hub
from schemas import CodeResponse

# ────────────────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────────────────
FASTLLM = "gpt-4o-mini"
LONGCONTEXTLLM = "o3-mini-2025-01-31"
QUESTION_VECTOR_STORE_PATH = r"ai_workspace\vectorstores\QUESTIONMOD_VS"
N_SEARCH_QUERIES = 3
CSV_PATH = r"data\QuestionDataV2_06122025_classified.csv"

fast_llm = ChatOpenAI(model=FASTLLM)
long_context_llm = ChatOpenAI(model=LONGCONTEXTLLM)

# ────────────────────────────────────────────────────────────────────────────────
# Vector store & retriever
# ────────────────────────────────────────────────────────────────────────────────
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

q_vectorstore = FAISS.load_local(
    QUESTION_VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
)

# Question retriever and formatter
q_retriever_js = SemanticExamplesCSV(
    column_names=["question.html", "server.js"],
    csv_path=CSV_PATH,
    vector_store=q_vectorstore,
)
q_retriever_py = SemanticExamplesCSV(
    column_names=["question.html", "server.js"],
    csv_path=CSV_PATH,
    vector_store=q_vectorstore,
)


# Define the state
class State(BaseModel):
    question_html: str
    solution_guide: Optional[str] = None
    isAdaptive: bool = True
    server_file: str = ""


def generate_server_js(state: State):
    # Retrieve the base prompt template from the hub
    base_prompt = hub.pull("server_js_template_base")

    if state.solution_guide:
        base_prompt += (
            "\n\nAdditionally, you are provided with the following solution guide. "
            "This solution guide outlines the intended approach and logic for solving the question. "
            "You must use the reasoning, steps, and methodology from this guide as the primary reference for how the question should be implemented and transformed into the JavaScript (server.js) file. "
            "Expand on the steps where necessary for clarity, but ensure that the structure and logic of the JavaScript output closely follow the solution guide's approach."
            f"\n\nSolution Guide:\n{state.solution_guide}\n"
        )

    q_retriever_js.set_filter({"isAdaptive": state.isAdaptive})
    prompt = q_retriever_js.format_template(
        query=state.question_html, k=1, base_template=base_prompt
    )

    # Generate the code response
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    messages = prompt.format_messages(question=state.question_html)  # type: ignore
    result = chain.invoke(messages)
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    return {"server_file": structured.code}


def generate_server_py(state: State):
    # Retrieve the base prompt template from the hub
    base_prompt = hub.pull("server_py_template_base1")

    if state.solution_guide:
        base_prompt += (
            "\n\nAdditionally, you are provided with the following solution guide. "
            "This solution guide outlines the intended approach and logic for solving the question. "
            "You must use the reasoning, steps, and methodology from this guide as the primary reference for how the question should be implemented and transformed into the JavaScript (server.js) file. "
            "Expand on the steps where necessary for clarity, but ensure that the structure and logic of the Python output closely follow the solution guide's approach."
            f"\n\nSolution Guide:\n{state.solution_guide}\n"
        )

    q_retriever_js.set_filter({"isAdaptive": state.isAdaptive})
    prompt = q_retriever_py.format_template(
        query=state.question_html, k=1, base_template=base_prompt
    )

    # Generate the code response
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    messages = prompt.format_messages(question=state.question_html)  # type: ignore
    result = chain.invoke(messages)
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    return {"server_file": structured.code}


# Workflow for server.js generation
workflow = StateGraph(State)
workflow.add_node("generate_server_js", generate_server_js)

workflow.add_edge(START, "generate_server_js")
workflow.add_edge("generate_server_js", END)
app = workflow.compile()

# Workflow for server.py generation
workflow_py = StateGraph(State)
workflow_py.add_node("generate_server_py", generate_server_py)

workflow_py.add_edge(START, "generate_server_py")
workflow_py.add_edge("generate_server_py", END)
app_py = workflow_py.compile()


if __name__ == "__main__":
    save_graph_visualization(
        app,  # type: ignore
        "serverjs_graph.png",
        base_path=r"ai_workspace/agentsv2/code_generator/ver3/graphs",
    )  #
    save_graph_visualization(
        app_py,  # type: ignore
        "serverpy_graph.png",
        base_path=r"ai_workspace/agentsv2/code_generator/ver3/graphs",
    )  #

    t_inputs = [
        {
            "question_html": """<pl-question-panel>\n  
            <p>A car is traveling along a straight road at a speed of {{params.initialSpeed}} {{params.unitsSpeed}}. 
            It sees a stop sign {{params.distanceToSign}} {{params.unitsDistance}} ahead and applies the brakes, coming to a complete stop just as it reaches the sign.</p>\n  <p>What is the car\'s constant acceleration during this process? Show your calculations.</p>\n</pl-question-panel>\n\n<pl-input-container>\n  
            <pl-number-input answers-name="initialSpeed" label="Initial Speed ({{params.unitsSpeed}})" />\n  <pl-number-input answers-name="distanceToSign" label="Distance to Stop Sign ({{params.unitsDistance}})" />\n</pl-input-container>\n\n<pl-number-input answers-name="acceleration" comparison="sigfig" digits="3" label="Acceleration (in {{params.unitsAcceleration}})"/>"""
        },
    ]

    for t in t_inputs:
        for chunk in app.stream(t, stream_mode="updates"):
            print(chunk)

    for t in t_inputs:
        for chunk in app_py.stream(t, stream_mode="updates"):
            print(chunk)
