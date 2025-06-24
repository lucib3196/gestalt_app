import asyncio
from typing import List
from pydantic import BaseModel, Field
from langchain import hub

from .ImageLLMProcessor import ImageLLMProcessor
from schemas import Question


class QuestionResponse(BaseModel):
    """
    Expected structured output from the image-based question extractor.
    """
    questions_payload: List[Question]
    num_extracted: int = Field(description="Number of questions that were identified")


def main():
    # Load the prompt from LangChain hub
    prompt = hub.pull("extract-all-questions")

    # Initialize the processor with the target model and output schema
    extractor = ImageLLMProcessor(
        prompt=prompt,
        schema=QuestionResponse,
        model="gpt-4o-2024-08-06"
    )

    # Define the image path(s) to extract questions from
    image_paths = [r"..\Images\handwritten\mass_block.png"]

    # Run the async request and print results
    results = asyncio.run(extractor.send_arequest(image_paths))
    print(results)


if __name__ == "__main__":
    main()
