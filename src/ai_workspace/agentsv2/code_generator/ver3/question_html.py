from collections.abc import Iterable
from itertools import chain
from typing import List, Literal

from langchain import hub
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from ai_workspace.retrievers import SemanticExamplesCSV
from ai_workspace.utils.helper import parse_structured, save_graph_visualization
from langgraph.graph import END, START, StateGraph

from schemas import CodeResponse

# ────────────────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────────────────
FASTLLM = "gpt-4o-mini"
LONGCONTEXTLLM = "o3-mini-2025-01-31"
TAG_VECTOR_STORE_PATH = r"ai_workspace\vectorstores\QUESTIONTAG_VS"
QUESTION_VECTOR_STORE_PATH = r"ai_workspace\vectorstores\QUESTIONMOD_VS"
N_SEARCH_QUERIES = 3
CSV_PATH = r"data\QuestionDataV2_06122025_classified.csv"

fast_llm = ChatOpenAI(model=FASTLLM)
long_context_llm = ChatOpenAI(model=LONGCONTEXTLLM)
# ────────────────────────────────────────────────────────────────────────────────
# Vector store & retriever
# ────────────────────────────────────────────────────────────────────────────────
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
tag_vectorstore = FAISS.load_local(
    TAG_VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
)
tag_retriever = tag_vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": N_SEARCH_QUERIES}
)

q_vectorstore = FAISS.load_local(
    QUESTION_VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
)

# Question retriever and formatter
q_retriever = SemanticExamplesCSV(
    column_names=["question", "question.html"],
    csv_path=CSV_PATH,
    vector_store=q_vectorstore,
)


## Query Generator
class Query(BaseModel):
    """A list of queries which will be used for the retrieval"""

    queries: List[str] = Field(..., description="A list of queries for searching")


llm_query = ChatOpenAI(model=FASTLLM)
structured_query = llm_query.with_structured_output(Query)
query_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""
You are an expert at generating effective search queries for academic databases of custom HTML tags used to generate academic content (quizzes, tests, homework, etc.).

Your task is to carefully analyze the user's question and generate up to **{N_SEARCH_QUERIES}concise and unique search queries**. These queries will be used to search a database of HTML tags relevant for rendering the question as an interactive HTML file.

When analyzing the question, focus on identifying key structural and functional aspects, such as:
- Is the question multiple choice, single choice, or open-ended?
- Does the question require a specific input type (e.g., checkbox, radio button, number input, text area)?
- Is the question multipart or does it contain sub-questions?
- Are there any special requirements (e.g., code input, mathematical expressions, file upload)?
- Any other relevant features that would influence the choice of HTML tags.

Guidelines:
- Focus on the **semantic intent** and structure of the question.
- Each query should:
    - Be direct, non-redundant, and reflect a different possible interpretation or aspect of the question.
    - Help identify the most relevant HTML tags for rendering the question appropriately.
    - Include keywords related to the input type, question structure, and any special requirements.
- The query should be focused on html tags you should be thinking as a developer who is trying to create 
a html file that will display these questions
""",
        ),
        (
            "human",
            "This is the input question to be converted to a html document \n Question: {question}",
        ),
    ]
)

query_generator = query_prompt | structured_query


## Retrieval grader
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: Literal["yes", "no"] = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


grade_documents_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert in educational technology and HTML development. Your task is to analyze the provided tag information (which describes custom HTML tags and their usage) and the given question (which needs to be converted into an interactive HTML format).

Determine if the tag information is directly useful and relevant for creating the HTML representation of the question. Consider whether the tag's functionality, input type, and features match the requirements of the question. If the tag information would help a developer implement the question as HTML, respond "yes". If it is not relevant or would not help, respond "no".
""",
        ),
        (
            "human",
            "Question to convert: {question}\nTag information: {documents}",
        ),
    ]
)

structured_grader = llm_query.with_structured_output(GradeDocuments)
grader = grade_documents_prompt | structured_grader


# Define the state
class State(BaseModel):
    question: str
    isAdaptive: bool = True
    queries: List[str] = Field(default_factory=list)
    tag_documents: List[Document] = Field(default=[])
    filtered_docs: List[Document] = Field(default=[])
    qfile: str = ""


# Nodees
def generate_queries(state: State):
    question = state.question
    question += q_retriever.format_template(
        query=question,
        k=2,
        base_template="\nAdditionally here are some examples of question formatted in html, these can aid in your search",
    )
    results = query_generator.invoke({"question": question})

    return {"queries": results.queries}  # type: ignore


def retrieve_tag_info(state: State):
    seen: set[str] = set()
    unique_docs: List[Document] = []
    for doc in chain.from_iterable(
        tag_retriever.invoke(q, filter={"type": "question"}) for q in state.queries
    ):
        t_name = doc.metadata.get("tag_name")

        if isinstance(t_name, str):
            tags = {t_name}
        elif isinstance(t_name, Iterable):
            tags = {str(t) for t in t_name}
        else:
            tags = {str(t_name)}
        # skip if we've already seen ANY of these tags
        if tags.isdisjoint(seen):
            seen.update(tags)
            unique_docs.append(doc)
    return {"tag_documents": unique_docs}


def generate_question_file(state: State):
    # Retrieve the base prompt template from the hub
    base_prompt = hub.pull("question_html_template")

    # Prepare tag documentation string
    tag_docs = "\n\n".join(
        f"- {doc.page_content}" for doc in (state.filtered_docs or state.tag_documents)
    )
    tag_info_section = (
        f"\n\nAdditionally, here is documentation for available tags you may reference:\n{tag_docs}"
        if tag_docs
        else ""
    )

    full_prompt = f"{base_prompt}{tag_info_section}"

    q_retriever.set_filter({"isAdaptive": state.isAdaptive})
    prompt = q_retriever.format_template(
        query=state.question, k=2, base_template=full_prompt
    )

    # Generate the code response
    chain = fast_llm.with_structured_output(CodeResponse, include_raw=True)
    result = chain.invoke([prompt])
    ai_message = result["raw"]
    structured = parse_structured(CodeResponse, ai_message)
    return {"qfile": structured.code}


# Current usage does not really need it as we have few tags may need to be added later on
# def grade_documents(state: State):
#     docs = state.tag_documents
#     filtered_docs = []
#     for d in docs:
#         score = grader.invoke({"question": state.question, "documents": d.page_content})
#         grade = score.binary_score  # type: ignore
#         if grade == "yes":
#             filtered_docs.append(d)
#         else:
#             continue
#     return {"filtered_docs": filtered_docs}


# Build the graph


workflow = StateGraph(State)
workflow.add_node("generate_search_queries", generate_queries)
workflow.add_node("retrieve_tag_info", retrieve_tag_info)
workflow.add_node("generate_question_file", generate_question_file)

workflow.add_edge(START, "generate_search_queries")
workflow.add_edge("generate_search_queries", "retrieve_tag_info")
workflow.add_edge("retrieve_tag_info", "generate_question_file")
workflow.add_edge("generate_question_file", END)
app = workflow.compile()


if __name__ == "__main__":
    save_graph_visualization(
        app,  # type: ignore
        "question_html_graph.png",
        base_path=r"ai_workspace/agentsv2/code_generator/ver3/graphs",
    )  #

    t_inputs = [
        {
            "question": "A car is traveling along a straight road at 20 m/s. It sees a stop sign 100 meters ahead and applies the brakes, coming to a complete stop just as it reaches the sign. What is the car's constant acceleration during this process? Show your calculations."
        },
        {
            "question": (
                "Part 1: What is the chemical symbol for water? Please enter your answer.\n"
                "Part 2: List the three states of matter and provide an example for each. Please enter your answers for each state."
            )
        },
        {
            "question": (
                "A robotics competition involves programming an autonomous robot to complete a series of tasks:\n"
                "Part 1: The robot must travel a distance of 2.5 meters in a straight line. Enter the minimum time (in seconds) required if its maximum speed is 0.5 m/s.\n"
                "Part 2: The robot must pick up an object and place it in one of three bins. Which bin should the robot choose if the object is metallic?\n"
                "A) Red bin (plastic)\n"
                "B) Blue bin (metal)\n"
                "C) Green bin (paper)\n"
                "Part 3: After sorting, the robot must rotate 90 degrees to face the next task. Enter the angle (in degrees) the robot must turn if it starts facing north and needs to face east."
            )
        },
    ]

    for t in t_inputs:
        for chunk in app.stream(t, stream_mode="updates"):
            print(chunk)
