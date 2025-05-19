import os
import json
import asyncio
from typing import List

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain import hub

from ...models.questionModels import Derivation
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


class Derivations(BaseModel):
    all_derivations: List[Derivation]

    @property
    def as_str(self) -> str:
        return "\n\n".join(derivation.as_str for derivation in self.all_derivations)


async def extract_derivations(image_paths: List[str], max_retries: int = 3):
    """
    Extracts questions from the provided image paths using an LLM processor.
    Retries up to `max_retries` times if response content is None or empty.
    """
    prompt = hub.pull("extract-computational-questions")
    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=Derivations,
        model=LONG_CONTEXT_MODEL,
    )

    attempt = 0
    questions = None
    ai_message = None

    while attempt < max_retries and not questions:
        response = await image_extraction.send_arequest_raw(image_paths)
        ai_message = response.get("raw")
        try:
            parsed = parse_structured(Derivations, ai_message)
            if parsed and parsed.all_derivations:
                derivations = parsed
                break
        except Exception as e:
            print(f"Parsing failed on attempt {attempt + 1}: {e}")
        attempt += 1

    if not derivations:
        raise ValueError("Failed to extract any valid questions after retries.")

    token_usage = extract_token_usage(ai_message, "extract_derivations")

    return {
        "derivations": derivations,
        "token_usage": [token_usage],
    }


async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path = (
        r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lec11-post.pdf"
    )
    pdf_directory = os.path.dirname(pdf_path)
    output_dir = os.path.join(pdf_directory, "lecture_images")
    os.makedirs(output_dir, exist_ok=True)

    image_paths = await pdf_to_image_persistent(pdf_path, output_dir)
    response = await extract_derivations(image_paths)

    derivations: Derivations = response["derivations"]
    token_usage = response["token_usage"]

    # Save Markdown
    with open(os.path.join(base_path, "derivations.md"), "w") as f:
        f.write("\n\n".join(d.as_str for d in derivations.all_derivations))

    # Save JSON
    with open(os.path.join(base_path, "derivations.json"), "w") as f:
        json.dump(to_serializable(response), f, indent=4)

    print(token_usage)


if __name__ == "__main__":
    asyncio.run(main())
