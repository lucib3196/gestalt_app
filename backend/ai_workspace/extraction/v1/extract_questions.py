import os
import json
import asyncio
from typing import List

from pydantic import BaseModel,Field
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


# ----------------------
# Models
# ----------------------
class AllQuestion(BaseModel):
    questions: List[Question] = Field(..., description="A list of complete question")
    
    @property
    def as_str(self)->str:
        return "\n\n".join(q.as_str for q in self.questions)


# ----------------------
# Core Function with Retry
# ----------------------
async def extract_questions(image_paths: List[str], max_retries: int = 3):
    """
    Extracts questions from the provided image paths using an LLM processor.
    Retries up to `max_retries` times if response content is None or empty.
    """
    prompt = hub.pull("extract-computational-questions")
    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=AllQuestion,
        model=LONG_CONTEXT_MODEL,
    )

    attempt = 0
    questions = None
    ai_message = None

    while attempt < max_retries and not questions:
        response = await image_extraction.send_arequest_raw(image_paths)
        ai_message = response.get("raw")
        try:
            parsed = parse_structured(AllQuestion, ai_message)
            if parsed and parsed.questions:
                questions = parsed
                break
        except Exception as e:
            print(f"Parsing failed on attempt {attempt + 1}: {e}")
        attempt += 1

    if not questions:
        raise ValueError("Failed to extract any valid questions after retries.")

    token_usage = extract_token_usage(ai_message, "extract_questions")

    return {
        "questions": questions,
        "token_usage": [token_usage],
    }


# ----------------------
# Entrypoint
# ----------------------
async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path = r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lec11-post.pdf"
    pdf_directory = os.path.dirname(pdf_path)
    output_dir = os.path.join(pdf_directory, "lecture_images")
    os.makedirs(output_dir, exist_ok=True)

    image_paths = await pdf_to_image_persistent(pdf_path, output_dir)
    response = await extract_questions(image_paths)

    questions: AllQuestion = response["questions"]
    token_usage = response["token_usage"]

    # Save Markdown
    with open(os.path.join(base_path, "questions.md"), "w") as f:
        f.write("\n\n".join(q.as_str for q in questions.questions))

    # Save JSON
    with open(os.path.join(base_path, "questions.json"), "w") as f:
        json.dump(to_serializable(response), f, indent=4)
        
    print(token_usage)


if __name__ == "__main__":
    asyncio.run(main())
