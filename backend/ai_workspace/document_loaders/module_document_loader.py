"""
Created on: March 25, 2025
Author: Luciano Bermudez

This script defines a custom document loader for LangChain that reads a CSV file containing
mechanical engineering-related questions and lazily yields them as LangChain-compatible `Document` objects.
Each document is extracted from the "question" column in the CSV and includes metadata such as its row index
and the source file path.

Useful for embedding pipelines, vector store generation, or LLM-powered content workflows.
"""

import os
import pandas as pd
from typing import Iterator
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

# Define the CSV path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'data', 'Question_Embedding_20241230.csv'))

class ModuleDocumentLoaderCSV(BaseLoader):
    """
    A custom LangChain loader that reads questions from a CSV file
    and yields them as Document objects.

    Attributes:
        file_path (str): Path to the CSV file.

    Methods:
        load_csv(): Loads the CSV file into a DataFrame.
        lazy_load(): Lazily yields Documents from the CSV rows.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_csv(self) -> None:
        """Loads the CSV file into a pandas DataFrame."""
        self.df = pd.read_csv(self.file_path)

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily loads each row from the DataFrame and yields it
        as a LangChain Document, skipping rows with missing content.
        """
        self.prepare_data()
        for index in self.df.index:
            content = self.df.loc[index, "question"]
            if pd.isna(content):
                continue

            yield Document(
                page_content=content,
                metadata={"source": self.file_path, "index": index, "isAdaptive":self.df.loc[index, "is_adaptive"]}
            )
    def prepare_data(self):
        """
        Loads the CSV data and sets the 'is_adaptive' column on a row-by-row basis.
        
        For each row, if both the 'server.js' and 'server.py' columns are either NaN or empty,
        then 'is_adaptive' is set to False; otherwise, it is set to True.
        
        This method assumes that the 'load_csv' method has been defined to load data into self.df.
        """
        self.load_csv()
        
        # Create a boolean mask where both 'server.js' and 'server.py' are either NaN or empty.
        mask = (
            (self.df["server.js"].isna() | (self.df["server.js"] == "")) &
            (self.df["server.py"].isna() | (self.df["server.py"] == ""))
        )
        
        # If the mask is True (both columns are empty/NaN), set 'is_adaptive' to False, else True.
        self.df["is_adaptive"] = (~mask).astype(str)



if __name__ == "__main__":
    loader = ModuleDocumentLoaderCSV(file_path)
    loader.prepare_data()
    docs = list(loader.lazy_load())
    print(f"Loaded {len(docs)} documents.\n")

    for doc in docs:
        print(type(doc))
        print(doc)
