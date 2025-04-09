# ------------------------
# 📦 Standard Library Imports
# ------------------------
import json
import os
from ast import literal_eval
from typing import Any, List, Literal, Optional, TypedDict

# ------------------------
# 🌐 Third-Party Imports
# ------------------------
from IPython.display import Image, display
from pydantic import BaseModel, Field

from langchain import hub
from langchain_core.runnables import chain as as_runnable, RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.pregel import RetryPolicy

# ------------------------
# 🤖 Language Models
# ------------------------
fast_llm = ChatOpenAI(model="gpt-4o-mini")  # Fast LLM for shorter tasks
long_context_llm = ChatOpenAI(model="gpt-4o")  # For complex inputs / long context

# ------------------------
# 📘 Input Schema: Question Payload
# ------------------------
class QuestionPayload(BaseModel):
    question: str = Field(
        description="The complete, standalone question intended for conversion into educational content."
    )
    solution_guide: Optional[str] = Field(
        default=None,
        description="A comprehensive, step-by-step explanation detailing the method to solve the question."
    )
    additional_instructions: Optional[str] = Field(
        default=None,
        description="Specific directives or preferences provided by the user regarding the presentation, constraints, or other aspects of the question."
    )

# ------------------------
# 📘 Output Schema: Metadata
# ------------------------
class QuestionMetadata(BaseModel):
    title: str
    question: str
    stem: str
    topic: str
    tags: List[str]
    prereqs: List[str]
    isAdaptive: Literal['True', 'False']

# ------------------------
# ⚙️ Runnable Chain: Generate Metadata
# ------------------------
@as_runnable
async def analyze_question_and_genmetadata(question: str):
    prompt = hub.pull("gestalt_metadata")
    chain = prompt | fast_llm.with_structured_output(QuestionMetadata)
    return await chain.ainvoke({"question": question})

# ------------------------
# 📦 State for Graph: Question Build Phase
# ------------------------
class QuestionBuildState(TypedDict):
    question_payload: QuestionPayload
    question_metadata: QuestionMetadata

# ------------------------
# 🔧 Node: Analyze Initial Question
# ------------------------
async def generate_metadata(state: QuestionBuildState):
    question = state["question_payload"].get("question")
    question_metadata = await analyze_question_and_genmetadata.ainvoke({"question": question})
    return {
        **state,
        "question_metadata": question_metadata,
    }

# ------------------------
# 🔁 Graph Construction
# ------------------------
question_builder = StateGraph(QuestionBuildState)
nodes = [
    ("generate_metadata", generate_metadata),
]

for i, (name, node) in enumerate(nodes):
    question_builder.add_node(name, node, retry=RetryPolicy(max_attempts=3))
    if i > 0:
        question_builder.add_edge(nodes[i - 1][0], name)

question_builder.add_edge(START, nodes[0][0])
question_builder.add_edge(nodes[-1][0], END)
question_builder = question_builder.compile()

# ------------------------
# 🖼️ Optional: Save Graph Visualization
# ------------------------
def save_graph_image(graph, filename="QuestionMetadataGraph.png"):
    try:
        image = graph.get_graph().draw_mermaid_png()
        display(Image(image))
        with open(os.path.join(os.path.dirname(__file__), filename), 'wb') as f:
            f.write(image)
            print(f"Saved Image at {filename}")
    except Exception as e:
        print(f"Graph visualization failed: {e}")

# ------------------------
# 🚀 Main Entry Point
# ------------------------
async def main():
    initial_state = {
        "question_payload": {
            "question": "What is the final velocity of a 2 kg projectile launched at 30 degrees with an initial speed of 20 m/s after 3 seconds?",
            "solution_guide": None,
            "additional_instructions": None,
        }
    }

    result = await question_builder.ainvoke(initial_state)
    print(result)

# ------------------------
# 🔓 Run if Script
# ------------------------
if __name__ == "__main__":
    save_graph_image(question_builder)
    import asyncio
    asyncio.run(main())
