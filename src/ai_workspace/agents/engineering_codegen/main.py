from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import os 
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from .example_template import ExampleBasedTemplate

question_base_template =r"""1. **Analyze the Question**  
   Determine if the physics question is computational or theoretical. This step dictates whether placeholders for numerical values are needed. Ensure accurate categorization by considering the context and specifics.
2. **Identify Parameters**  
   For computational questions, identify all numerical values essential for calculations. Replace these values with placeholders in the format `{{params.variable_name}}` using clear, descriptive names to avoid confusion.
3. **Implement Placeholders**  
   Replace every numerical value in the question with placeholders, allowing dynamic interaction in the HTML. For example, "100 meters" and "5 seconds" become `{{params.distance}}` and `{{params.time}}`.
4. **Review Examples**  
   Analyze the provided examples to understand best practices for placeholder use. Adapt these to your question to ensure variables can be manipulated for interactive results.
5. **Include Files Only with Direct Path**  
   Only include files if their direct path is provided.
6. Enhance Formatting
- Use appropriate HTML tags to improve readability and structure:
  - **Lists**:
    - Use `<ul>` for unordered points (e.g., properties or conditions).
    - Use `<ol>` for ordered steps or procedures.
  - **Emphasis**:
    - Use `<strong>` or `<b>` to highlight key terms, variables, and important values.
    - Use `<i>` for emphasis on explanations or theoretical concepts.
  - **Line Breaks**:
    - Use `<br>` for logical breaks to avoid long, unreadable paragraphs.
  - **Tables (if applicable)**:
    - Organize complex data or parameters into tables using `<table>`, `<thead>`, and `<tbody>`."""
    

question_html_builder = ExampleBasedTemplate(["question","question.html"], base_template=question_base_template)


class State(TypedDict):
    messages:Annotated[list, add_messages]

llm = ChatOpenAI()
def chatbot(state:State):
    return {"messages":llm.invoke(state["messages"])}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        print(event)

user_input = question_html_builder.generate_prompt("A car is traveling across a road at a constant speed of 50 mph calculate the total distance traveled")     
print(user_input)
stream_graph_updates(user_input=user_input)