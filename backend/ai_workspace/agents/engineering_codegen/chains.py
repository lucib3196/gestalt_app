from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessageGraph, MessagesState
from pydantic import BaseModel,Field
from typing import Annotated
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict



llm = ChatOpenAI(model="gpt-4o")

