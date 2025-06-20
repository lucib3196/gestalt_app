from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from langchain import hub
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.pregel import RetryPolicy  # type: ignore

from ai_workspace.utils import (
    parse_structured,
    save_graph_visualization,
)
from ai_workspace.agentsv2.question_topic_classification_agent.question_topic_classification_agent import (
    app as topic_classifier,
)
from ai_workspace.agentsv2.course_classification_agent.course_classification_agent import (
    app as course_classification,
)
from ai_workspace.agentsv2.course_classification_agent.course_classification_agent import (
    CourseClassification,
)
from schemas import InitialMetadata

# ────────────────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────────────────
FASTLLM = "gpt-4o-mini"
fast_llm = ChatOpenAI(model=FASTLLM)


# ────────────────────────────────────────────────────────────────────────────────
# State Models
# ────────────────────────────────────────────────────────────────────────────────
class MetadataInput(BaseModel):
    question: str
    initial_metadata: Optional[InitialMetadata] = Field(
        None, title="Initial Metadata from the user"
    )


class MetadataState(BaseModel):
    question: str = Field(default="")
    title: str = Field(default="")
    topic: List[str] = Field(default=[])
    relevant_courses: List[str] = Field(default=[])
    tags: List[str] = Field(default=[])
    prereqs: List[str] = Field(default=[])
    isAdaptive: Optional[Literal["True", "False"]] = None


class QuestionMetadata(BaseModel):
    title: str = Field(..., description="A concise title summarizing the question.")
    stem: str = Field(
        ..., description="Background or scenario text that frames the question."
    )
    tags: List[str] = Field(
        ..., description="A list of keywords for categorization and filtering."
    )
    prereqs: Optional[List[str]] = Field(
        None,
        description="Math or Engineering prerequisites that are required to understand and solve the problem.",
    )
    isAdaptive: Literal["True", "False"] = Field(
        ...,
        description="Whether the question is adaptive (requires computation and a backend) or non-adaptive (e.g., multiple choice).",
    )


# ────────────────────────────────────────────────────────────────────────────────
# Node Functions
# ────────────────────────────────────────────────────────────────────────────────
def classify_question(state: MetadataInput) -> MetadataState:
    metadata_prompt = hub.pull("gestalt_metadata")
    chain = metadata_prompt | fast_llm.with_structured_output(
        QuestionMetadata, include_raw=True
    )
    result = chain.invoke({"question": state.question})
    ai_message = result["raw"]
    question_metadata = parse_structured(QuestionMetadata, ai_message)
    return {
        "title": question_metadata.title,
        "tags": question_metadata.tags,
        "prereqs": question_metadata.prereqs if question_metadata.prereqs else [],
        "isAdaptive": question_metadata.isAdaptive,
    }  # type: ignore


def classify_question_topic(state: MetadataInput) -> MetadataState:
    topics = topic_classifier.invoke({"question": state.question})
    return {"topic": topics.get("topic_classification_result").topics}  # type: ignore


def classify_question_courses(state: MetadataInput) -> MetadataState:
    relevant_courses = course_classification.invoke({"question": state.question})

    return {"relevant_courses": relevant_courses.get("generation", CourseClassification(course_id=[])).course_id}  # type: ignore


# ────────────────────────────────────────────────────────────────────────────────
# Graph Construction
# ────────────────────────────────────────────────────────────────────────────────
graph = StateGraph(MetadataState, input=MetadataInput)
nodes = [
    ("classify_question_topic", classify_question_topic),
    ("generate_metadata_legacy", classify_question),
    ("classify_question_courses", classify_question_courses),
]
for name, func in nodes:
    graph.add_node(name, func, retry=RetryPolicy(max_attempts=1))

graph.add_edge(START, "classify_question_topic")
graph.add_edge(START, "classify_question_courses")
graph.add_edge(START, "generate_metadata_legacy")

graph.add_edge("classify_question_topic", END)
graph.add_edge("classify_question_courses", END)
graph.add_edge("generate_metadata_legacy", END)

compiled_graph = graph.compile()


# ────────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────────
def main():
    save_graph_visualization(
        compiled_graph,  # type: ignore
        filename="QuestionMetadata.png",
        base_path=r"ai_workspace/agentsv2/code_generator/ver3/graphs",
    )
    question = "A car is traveling along a straight road at 60 mph; calculate distance after 4 hours"
    input_state = MetadataInput(question=question, initial_metadata=None)  # type: ignore
    for chunk in compiled_graph.stream(input_state, stream_mode="updates"):
        print(chunk)


if __name__ == "__main__":
    main()
