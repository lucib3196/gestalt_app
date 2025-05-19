import os
import json
import asyncio
from typing import List

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain import hub

from ...models.questionModels import LectureSummary
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
# Prompt Templates
# ----------------------
lecture_extraction_prompt = """# **Prompt for Analyzing Lecture Content**
You are tasked with analyzing the **entire provided lecture material** from an engineering, physics, or mathematics class. Your goal is to create a **structured analysis** that captures essential information and organizes it clearly.  
Return the results as a structured JSON object with the following fields:

---

### **1. Lecture Title**
- Generate a **clear and concise title** that accurately reflects the overall focus of the lecture.
- The title should summarize the **main ideas or themes** presented.
- **Field**: `lecture_name: str`

---

### **2. Key Takeaways**
- Identify the **major principles, laws, formulas, and methods** introduced in the lecture.
- For each key takeaway:
  - Create a **section title** that names the principle, law, or formula.
  - Provide a **short description** explaining its meaning, importance, and possible applications.
  - Include **LaTeX formatting** (delimited with `$`) for any mathematical symbols, equations, or important expressions.
- **Field**: `key_takeaways: List[Section]`

---

### **3. Learning Objectives**
- Extract the **primary learning goals** for students.
- For each objective:
  - Write a **section title** summarizing what the student should be able to understand or perform after the lecture.
  - Provide a **brief description** explaining the competency or understanding expected.
  - Focus on **what students should know, calculate, apply, or reason through** after the lecture.
- **Field**: `learning_objectives: List[Section]`

---

### **4. Technical Concepts**
- Identify **technical topics** introduced in the lecture, such as:
  - Definitions of terms
  - Laws and physical principles
  - Key derivations and important formulas
- For each technical concept:
  - Provide a **section title** naming the concept or law.
  - Write a **short but informative description** that explains the concept clearly.
  - Use **LaTeX formatting** for any equations or technical notation.
- **Field**: `technical_concepts: List[Section]`

---

# **Important Notes**
- Ensure all content is **accurate, clear, and structured**.
- **Use LaTeX** (`$...$`) for all mathematical content (equations, variables, technical expressions).
- The output must strictly follow the JSON structure of the provided fields.
- Write in a style that is **both technically precise and easy to understand** for engineering, physics, and math students.

---
"""


# ----------------------
# Core Function with Retry
# ----------------------
async def extract_summary(image_paths: List[str], max_retries: int = 3):
    """
    Extracts questions from the provided image paths using an LLM processor.
    Retries up to `max_retries` times if response content is None or empty.
    """
    prompt = hub.pull("extract-computational-questions")
    image_extraction = ImageLLMProcessor(
        prompt=prompt,
        include_raw=True,
        schema=LectureSummary,
        model=LONG_CONTEXT_MODEL,
    )

    attempt = 0
    questions = None
    ai_message = None

    while attempt < max_retries and not questions:
        response = await image_extraction.send_arequest_raw(image_paths)
        ai_message = response.get("raw")
        try:
            parsed = parse_structured(LectureSummary, ai_message)
            if parsed and parsed:
                summary = parsed
                break
        except Exception as e:
            print(f"Parsing failed on attempt {attempt + 1}: {e}")
        attempt += 1

    if not summary:
        raise ValueError("Failed to extract any valid summary after retries.")

    token_usage = extract_token_usage(ai_message, "extract_summary")

    return {
        "lecture_summary": summary,
        "token_usage": [token_usage],
    }


# ----------------------
# Entrypoint
# ----------------------
async def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path = (
        r"C:\Users\lberm\OneDrive\Documents\Github\gestalt_app\Lectures\Lec11-post.pdf"
    )
    pdf_directory = os.path.dirname(pdf_path)
    output_dir = os.path.join(pdf_directory, "lecture_images")
    os.makedirs(output_dir, exist_ok=True)

    image_paths = await pdf_to_image_persistent(pdf_path, output_dir)
    response = await extract_summary(image_paths)

    lecture_summary: LectureSummary = response["lecture_summary"]
    token_usage = response["token_usage"]

    # Save Markdown
    with open(os.path.join(base_path, "lecture_summary.md"), "w") as f:
        f.write(lecture_summary.as_str)

    # Save JSON
    with open(os.path.join(base_path, "lecture_summary.json"), "w") as f:
        json.dump(to_serializable(response), f, indent=4)

    print(token_usage)


if __name__ == "__main__":
    asyncio.run(main())
