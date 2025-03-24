from typing import Annotated
from typing_extensions import TypedDict
import os

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
import asyncio

# Define the state 
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Define the LLM 
llm = ChatOpenAI()

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

# Build the graph 
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()



# Save the graph 
filename = "simple_chat.png"
current_dir= os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(current_dir, filename)
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
    with open(filepath, 'wb') as f:
        f.write(graph.get_graph().draw_mermaid_png())
        print(f'Saved Image at {filepath}')
except Exception:
    pass

# Function to run the graph
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},
        stream_mode="values",):
        event["messages"][-1].pretty_print()

async def main():
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)
        except:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break

if __name__ == "__main__":
    asyncio.run(main())