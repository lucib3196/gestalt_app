"""
Created on: March 25, 2025
Author: Luciano Bermudez

This module defines the ExampleBasedTemplate class, which uses a semantic search mechanism
to extract examples from a CSV file and format them into a prompt. The class leverages the 
SemanticExamples class (imported from semantic_search) to retrieve example pairs. The 
column_names parameter should be a list of two strings: the first is the input column and the 
second is the output column.
"""

from .semantic_search import SemanticExamples

class ExampleBasedTemplate:
    """
    A template class that generates a prompt by combining a base template with example pairs 
    extracted via semantic search.

    Attributes:
        semantic_search (SemanticExamples): An instance of SemanticExamples for retrieving examples.
        base_template (str): The base text template to which the examples will be appended.
    """
    
    def __init__(self, column_names: list[str], base_template: str) -> None:
        """
        Initializes the ExampleBasedTemplate with the specified column names and base template.
        
        Args:
            column_names (list[str]): A list of two column names [input_column, output_column].
            base_template (str): The base prompt text.
        """
        self.semantic_search = SemanticExamples(column_names)
        self.base_template = base_template
    
    def extract_examples(self, query: str, k: int = 2) -> str:
        """
        Extracts examples based on the provided query, formats them, and appends them to the base template.
        
        Args:
            query (str): The query string to search for similar examples.
            k (int): The number of top results to retrieve (default is 2).
            
        Returns:
            str: The complete prompt consisting of the base template followed by the formatted examples.
        """
        examples = self.semantic_search.extract_examples(query, k)
        formatted_examples = ""
        for ex in examples:
            formatted_examples += f"Input: {ex[0]}\nOutput: {ex[1]}\n"
        prompt = f"{self.base_template}\n{formatted_examples}"
        return prompt

if __name__ == "__main__":
    # Define the base template and column names
    base_template = "Write code for the following"
    # "question" is assumed to be the input column and "question.html" the output column.
    gen_prompt = ExampleBasedTemplate(["question", "question.html"], base_template)
    
    # Generate a prompt based on a sample query
    prompt = gen_prompt.extract_examples(
        "A car is traveling at a constant speed of 50mph. What is the total distance after 2 hours"
    )
    print(prompt)
