"""
Created on: March 25, 2025
Author: Luciano Bermudez

This module defines the SemanticExamples class, which creates examples from a CSV file
by using a vector store (via Chroma and OpenAI embeddings) to perform similarity search.
The column_names parameter should be a list of two strings:
    [input_column, output_column]
"""

import os
import pandas as pd
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Define the file path to the question CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'data', 'Question_Embedding_20241230.csv'))

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Load the vector store from a persistent directory
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "module_vectorstore")
vector_store = Chroma(
    collection_name="module_questions",
    embedding_function=embeddings,
    persist_directory=PERSIST_DIRECTORY
)

class SemanticExamples:
    """
    Creates semantic examples by performing similarity searches on a CSV-based vector store.
    
    The class reads a CSV file and uses a vector store to find similar examples based on a query.
    The CSV is expected to contain at least two columns specified by `column_names`,
    where the first column is the input and the second column is the output.
    
    Attributes:
        df (pd.DataFrame): DataFrame loaded from the CSV.
        vector_store (Chroma): Vector store used for similarity searches.
        column_names (list[str]): List of two column names: [input_column, output_column].
    """
    
    def __init__(self, column_names: list[str], csv_path: str = FILE_PATH, vector_store: Chroma = vector_store) -> None:
        if len(column_names) != 2:
            raise ValueError("column_names must be a list of two column names: [input_column, output_column].")
        self.df = pd.read_csv(csv_path)
        self.vector_store = vector_store
        self.column_names = column_names

    def extract_examples(self, query: str, k: int = 2) -> list[tuple]:
        """
        Extracts examples from the CSV based on a similarity search using the vector store.
        
        Args:
            query (str): The query to search for similar examples.
            k (int): The number of top results to retrieve (default is 2).
        
        Returns:
            List of tuples: Each tuple contains (input_example, output_example, index).
        """
        idxs = self.extract_index(query, k=k)
        if not self.is_valid_columns(self.df, self.column_names):
            return []
        
        examples = []
        for idx in idxs:
            input_example = self.df.loc[idx, self.column_names[0]]
            output_example = self.df.loc[idx, self.column_names[1]]
            examples.append((input_example, output_example, idx))
        return examples

    def extract_index(self, query: str, k: int = 2) -> list:
        """
        Performs a similarity search on the vector store and extracts the CSV indices from the results.
        
        Args:
            query (str): The query string.
            k (int): The number of top results to retrieve.
            
        Returns:
            List of indices extracted from the metadata of the results.
        """
        results = self.vector_store.similarity_search(query, k=k)
        indexes = [r.metadata["index"] for r in results]
        return indexes

    def extract_examples_prettyprint(self, query: str, k: int = 2) -> None:
        """
        Extracts examples and prints them in a human-readable format.
        
        Args:
            query (str): The query string.
            k (int): The number of top results to retrieve.
        """
        examples = self.extract_examples(query, k)
        print(f"Extracted Examples for: '{query}'\n")
        print("-" * 120)
        for input_ex, output_ex, idx in examples:
            print(f"CSV Index {idx}")
            print(f"Input:  {input_ex}\nOutput: {output_ex}")
            print("-" * 120)

    def is_valid_columns(self, df: pd.DataFrame, columns: list[str]) -> bool:
        """
        Checks if all specified columns exist in the DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame to check.
            columns (list[str]): List of column names to validate.
        
        Returns:
            True if all columns are valid, False otherwise.
        """
        invalid_columns = [column for column in columns if not self.is_valid_column(df, column)]
        if invalid_columns:
            print(f"Columns {invalid_columns} are not valid.")
            return False
        return True

    def is_valid_column(self, df: pd.DataFrame, column_to_check: str) -> bool:
        """
        Checks if a specific column exists in the DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame to check.
            column_to_check (str): The column name to validate.
        
        Returns:
            True if the column exists, False otherwise.
        """
        return column_to_check in df.columns

    
if __name__ =="__main__":
    columns_names = ["question", "question.html"]
    example_formatter = SemanticExamples(column_names=columns_names)
    
    query = "A car travels a total distance of 100 miles in 5 hours. Calculate its speed"
    print(example_formatter.extract_examples_prettyprint(query, 2))