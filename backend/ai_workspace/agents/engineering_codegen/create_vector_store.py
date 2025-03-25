"""
Created on: March 25, 2025
Author: Luciano Bermudez

This script creates a vector store using LangChain + ChromaDB from a CSV file 
containing mechanical engineering-related questions. It loads the questions, embeds them 
using OpenAI's embedding model, and stores them in a persistent Chroma vector store 
to enable fast similarity searches.
"""

import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from ...document_loaders.module_document_loader import ModuleDocumentLoaderCSV

# Define the file path to the question CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'Question_Embedding_20241230.csv'))

# Load documents from the CSV file
loader = ModuleDocumentLoaderCSV(file_path)
docs = list(loader.lazy_load())

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Create (and persist) Chroma vector store
persist_directory = os.path.join(BASE_DIR, "module_vectorstore")
vector_store = Chroma(
    collection_name="module_questions",
    embedding_function=embeddings,
    persist_directory=persist_directory
)

# Add documents to vector store
vector_store.add_documents(documents=docs)

if __name__ == '__main__':
    # Example similarity search query
    results = vector_store.similarity_search(
        "A car travels a total distance of 100 miles in 2 hours assuming the car is traveling at a constant speed. Determine its speed"
    )
    print(results)
