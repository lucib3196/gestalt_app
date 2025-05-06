import os
import json
import asyncio
from typing import List, Tuple, Annotated,Optional

from pydantic import BaseModel, Field, AfterValidator
from langchain_openai import ChatOpenAI
from langchain import hub


from ...models.questionModels import Question
from ...utils.helper import (
    extract_token_usage,
    parse_structured,
    pdf_to_image_persistent,
    to_serializable,
)
from ...image_processing.ImageLLMProcessor import ImageLLMProcessor

# ----------------------
# Constants & LLM Clients
# ----------------------
FAST_MODEL = "gpt-4o-mini"
LONG_CONTEXT_MODEL = "gpt-4.1"

fast_llm = ChatOpenAI(model=FAST_MODEL)
long_context_llm = ChatOpenAI(model=LONG_CONTEXT_MODEL)


def check_len(vals: list):
    if len(vals) > 2:
        raise ValueError(f"{vals} should only have 2 elements")
    return vals


# Define a generic range model
class PageRange(BaseModel):
    range: Annotated[List[int], check_len] = Field(
        ..., description="A list with the start and end page numbers"
    )


class PageRangeOutput(BaseModel):
    ranges: List[PageRange] = Field(
        ..., description="A list of page ranges for the specified content"
    )


async def extract_content_ranges(
    image_paths: list[str], prompt: str, schema: BaseModel, model: str, step_name:Optional[str]=None
):
    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=schema,
        model=model,
    )
    response = await image_extraction.send_arequest_raw(image_paths)
    ai_message = response.get("raw")
    content_ranges = parse_structured(schema, ai_message)
    token_usage = extract_token_usage(ai_message, step_name if step_name else "extract_content_ranges" )

    sep_imgpaths = []
    for r in content_ranges.ranges:
        val = r.range
        sep_imgpaths.append(image_paths[val[0] : val[1] + 1])

    return {
        "content_ranges": content_ranges,
        "sep_imgpaths": sep_imgpaths,
        "token_usage": [token_usage],
    }


async def extract_derivation_ranges(image_paths: list[str]):
    prompt = """
    You are tasked with identifying the page ranges that contain individual mathematical derivations within a document.
    Each entry in your output should represent a single derivation and include its full context.

    Important:
    - A **derivation** involves a sequence of logical or mathematical steps used to derive an equation, formula, or result.
    - A **question**, even if it contains math, is a problem to be solved and is not considered a derivation.
    - Do **not** include questions or problems in your output—only include actual derivations.

    Guidelines:
    - If multiple derivations appear on the same page, that's acceptable—return a separate range for each one.
    - If a derivation spans multiple pages, include all relevant pages in the range.
    - Do not group multiple derivations into a single range.

    Return the output as a list of page ranges in the format:
    {"range": [start_page, end_page]}

    """
    return await extract_content_ranges(
        image_paths=image_paths,
        prompt=prompt,
        schema=PageRangeOutput,
        model=LONG_CONTEXT_MODEL,
        step_name="extract_derivations_ranges"
    )

async def extract_question_ranges(image_paths: list[str]):
    prompt = """
    You are tasked with identifying the page ranges that contain individual questions within a document. Your goal is to determine the start and end pages for each question, 
    including any associated solutions if present.
    Only return the page ranges where there is an actual question
    There may be multiple questions per page, and that's acceptable.
    Each entry in your output should represent a single question and its full context (e.g., the question and solution if available).
    Return a list of page ranges in the format:

    {"question_range": [start_page, end_page]}


    This task is a preliminary analysis to segment the document into individual question blocks for further processing.
        """
    return await extract_content_ranges(
    image_paths=image_paths,
    prompt=prompt,
    schema=PageRangeOutput,
    model=LONG_CONTEXT_MODEL,
    step_name="extract_question_ranges",
)
    
    
async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path = r"Lectures\Lec11-post.pdf"
    pdf_directory = os.path.dirname(pdf_path)
    output_dir = os.path.join(pdf_directory, "document_images")
    os.makedirs(output_dir, exist_ok=True)

    image_paths = await pdf_to_image_persistent(pdf_path, output_dir, annotate=True)
    
    question_response = await extract_question_ranges(image_paths)
    # derivation_response = await extract_derivation_ranges(image_paths)
    
    print("Question Ranges:\n\n", question_response,"\n\n")
    # print("Derivation Ranges:\n\n", derivation_response,"\n\n")
    
if __name__ == "__main__":
    asyncio.run(main())