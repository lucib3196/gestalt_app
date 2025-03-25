from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import os 
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import pandas as pd


# Define the file path to the question CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'Question_Embedding_20241230.csv'))

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# Load Vector Store
persist_directory = os.path.join(BASE_DIR, "module_vectorstore")
vector_store = Chroma(
    collection_name="module_questions",  # Same collection name
    embedding_function=embeddings,
    persist_directory=persist_directory
)

def get_example(query:str, filepath:str, vector_store, k:int=2):
    df = pd.read_csv(file_path)
    results = vector_store.similarity_search(query,k)
    for r in results:
        index = r.metadata["index"]
        print(df.loc[index,"question.html"])
    
    
get_example("What is transport phenomena", filepath=file_path, vector_store=vector_store)   
# Define the State 
class State(TypedDict):
    messages:Annotated[list, add_messages]

