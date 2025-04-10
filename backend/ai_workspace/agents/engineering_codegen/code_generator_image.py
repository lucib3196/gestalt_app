import os
import asyncio
from typing import List

from pydantic import BaseModel, Field
from langchain import hub
from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy
from IPython.display import Image, display
from typing import Optional

from ...image_processing.ImageLLMProcessor import ImageLLMProcessor
from .code_generator import compiled_graph as question_formatter, InitialMetadata
from .code_generator import QuestionPayload, QuestionPackage


# -------------------- State Models --------------------

class QuestionExtractionResult(BaseModel):
    """
    Expected structured output from the image-based question extractor.
    """
    questions_payload: List[QuestionPayload]
    num_extracted: int = Field(description="Number of questions identified")


class ImageInputState(BaseModel):
    """
    Initial state: user provides a list of image paths.
    """
    image_paths: List[str]
    initial_metadata: Optional[InitialMetadata] = None


class ImageExtractionOutputState(BaseModel):
    """
    Output state: extracted and processed questions from the images.
    """
    image_paths: List[str]
    question_packages: List[QuestionPackage]
    num_extracted: int


# -------------------- Core Node Function --------------------

async def extract_and_format_questions(state: ImageInputState) -> ImageExtractionOutputState:
    """
    Uses an LLM to extract questions from images and then formats them.
    """
    prompt = hub.pull("extract-all-questions")
    
    extractor = ImageLLMProcessor(
        prompt=prompt,
        schema=QuestionExtractionResult,
        model="gpt-4o-2024-08-06"
    )

    extraction_result = await extractor.send_arequest(image_paths=state.image_paths)
    raw_payloads = extraction_result.get("questions_payload", [])

    # Process each payload using the question_formatter graph
    initial_metadata = state.initial_metadata
        
    format_tasks = [question_formatter.ainvoke({"question_payload": payload,"initial_metadata": initial_metadata}) for payload in raw_payloads]
    formatted_questions = await asyncio.gather(*format_tasks)

    return ImageExtractionOutputState(
        image_paths=state.image_paths,
        question_packages=formatted_questions,
        num_extracted=extraction_result.get("num_extracted", len(raw_payloads))
    )


# -------------------- LangGraph Setup --------------------

graph = StateGraph(ImageExtractionOutputState, input=ImageInputState, output=ImageExtractionOutputState)

graph.add_node("extract_and_format", extract_and_format_questions, retry=RetryPolicy(max_attempts=3))

graph.add_edge(START, "extract_and_format")
graph.add_edge("extract_and_format", END)

graph = graph.compile()


# -------------------- Graph Visualization --------------------

def save_graph_visualization(graph: StateGraph, filename: str = "ImageCodeBuilder.png") -> None:
    """
    Visualizes the graph and saves it as a PNG image.

    Args:
        graph: The StateGraph instance.
        filename: The filename to save the image.
    """
    try:
        image_bytes = graph.get_graph().draw_mermaid_png()
        display(Image(image_bytes))
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, "wb") as file:
            file.write(image_bytes)
        print(f"Saved graph visualization at {filename}")
    except Exception as error:
        print(f"Graph visualization failed: {error}")


# -------------------- Run --------------------

if __name__ == "__main__":
    save_graph_visualization(graph)

    # Example usage
    # image_paths = [r"backend\ai_workspace\image_processing\Screenshot 2024-08-21 191637.png"]
    # result = asyncio.run(graph.ainvoke({"image_paths": image_paths}))
    # print(result)
