import os
import json
import asyncio
from typing import Optional, List

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from ..image_processing.ImageLLMProcessor import ImageLLMProcessor
from ..utils.models import StepTokenUsage, TokenUsage
from ..utils.helper import pdf_to_image_persistent
from .models import Section

# ----------------------
# Constants
# ----------------------

FAST_MODEL = "gpt-4o-mini"
LONG_CONTEXT_MODEL = "gpt-4o"

fast_llm = ChatOpenAI(model=FAST_MODEL)
long_context_llm = ChatOpenAI(model=LONG_CONTEXT_MODEL)


# ----------------------
# Pydantic Models
# ----------------------
class Outline(BaseModel):
    page_title: str = Field(..., title="Title of the Wikipedia page")
    sections: List[Section] = Field(
        default_factory=list, title="Titles and descriptions for each section."
    )

    @property
    def as_str(self) -> str:
        sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.page_title}\n\n{sections}".strip()


class LectureSummary(BaseModel):
    lecture_outline: Outline


# ----------------------
# Prompt Templates
# ----------------------

lecture_summary_prompt = """
You are a Professor at a University tasked with writing a 
Wikipedia-style article based on the following lecture notes. 
Write an outline for a Wikipedia page about the lecture. Be comprehensive and specific.
"""

# ----------------------
# Chains
# ----------------------


async def generate_lecture_summary(image_paths: List[str]):
    """Generates a lecture summary based on analyzed lecture content."""
    image_extraction = ImageLLMProcessor(
        prompt=lecture_summary_prompt,
        include_raw=True,
        schema=LectureSummary,
        model=LONG_CONTEXT_MODEL,
    )
    response = await image_extraction.send_arequest_raw(image_paths)

    # Extract content
    ai_message = response["raw"]
    lecture_summary = LectureSummary(**json.loads(ai_message.content))

    # Extract token usage
    token_usage_data = ai_message.response_metadata.get("token_usage", {})

    return {
        "lecture_summary": lecture_summary,
        "token_usage": [
            StepTokenUsage(
                step_name="initial_analysis", token_usage=TokenUsage(**token_usage_data)
            )
        ],
    }


# ----------------------
# Main Execution
# ----------------------


async def main():
    pdf_path = r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lecture_02_03.pdf"
    pdf_directory = os.path.dirname(pdf_path)
    persistant_directory = os.path.join(pdf_directory, "lecture_images")
    os.makedirs(persistant_directory, exist_ok=True)

    image_paths = await pdf_to_image_persistent(pdf_path, persistant_directory)
    response = await generate_lecture_summary(image_paths)

    lecture_summary: LectureSummary = response["lecture_summary"]
    lecture_outline = lecture_summary.lecture_outline.as_str
    print(lecture_outline)


if __name__ == "__main__":
    asyncio.run(main())
