from ai_workspace.agentsv2.code_generator.ver3.code_generator import (
    compiled_graph as code_generator,
    CodeGenInput,
    CodeOutput,
)
from ai_workspace.agentsv2.image_processing.ImageLLMProcessor import ImageLLMProcessor
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from schemas import Question
from langchain import hub
import asyncio
from ai_workspace.utils import (
    save_graph_visualization,
    keep_first,
    merge_files_data,
    keep_new,
    to_serializable,
)
from schemas import InitialMetadata
from typing import Union
from langgraph.pregel import RetryPolicy  # type: ignore


# Response model for image processor
class QuestionResponse(BaseModel):
    """
    Expected structured output from the image-based question extractor.
    """

    questions_payload: List[Question]
    num_extracted: int = Field(description="Number of questions that were identified")


class StateInput(BaseModel):
    image_paths: List[str]
    initial_metadata: Union[dict[str, Any], InitialMetadata]


class StateIntermediate(BaseModel):
    extraction: QuestionResponse
    initial_metadata: Union[dict[str, Any], InitialMetadata]


class StateOutput(BaseModel):
    output: List[CodeOutput]


async def extract_question(state: StateInput) -> StateIntermediate:
    """
    Extract questions from images using the ImageLLMProcessor.
    """

    # Load the prompt from LangChain hub
    prompt = hub.pull("extract-all-questions")

    # Initialize the processor with the target model and output schema
    extractor = ImageLLMProcessor(
        prompt=prompt, schema=QuestionResponse, model="gpt-4o-2024-08-06"
    )

    # Await the results of the asynchronous image processing task
    results = await extractor.send_arequest(state.image_paths)
    return {"extraction": results, "initial_metadata": state.initial_metadata}  # type: ignore


async def generate_code(state: StateIntermediate) -> StateOutput:
    """
    Generate code based on the extracted questions.
    """

    payload = state.extraction.questions_payload

    # Create a list of async tasks for generating code for each question
    tasks = [
        code_generator.ainvoke(
            CodeGenInput(question_payload=q, initial_metadata=state.initial_metadata)
        )
        for q in payload
    ]

    # Gather all the results asynchronously
    results = await asyncio.gather(*tasks)
    return {"output": results}


graph = StateGraph(StateOutput, input=StateInput)

# Register nodes
graph.add_node(
    "extract_questions",
    extract_question,
    retry=RetryPolicy(max_attempts=1),
)
graph.add_node(
    "generate_code",
    generate_code,
    retry=RetryPolicy(max_attempts=1),
)
graph.add_edge(START, "extract_questions")
graph.add_edge("extract_questions", "generate_code")
graph.add_edge("generate_code", END)
compiled_graph = graph.compile()


if __name__ == "__main__":
    print("Running")
    save_graph_visualization(
        compiled_graph,  # type: ignore
        filename="MultiModalCodeGeneratorV3.png",
        base_path=r"ai_workspace/agentsv2/image_codegenerator",
    )

    # Test
    image_paths = [r"..\Images\handwritten\mass_block.png"]
    input_q = StateInput(image_paths=image_paths, initial_metadata=None)
    results = asyncio.run(compiled_graph.ainvoke(input_q))
    print(results)
