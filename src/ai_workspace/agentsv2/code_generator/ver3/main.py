import os
import json
import asyncio
from typing import List
from .code_generator import compiled_graph as code_generator_v3
from .code_generator import CodeGenInput, CodeGenOutput
from schemas import Question
from ai_workspace.utils import to_serializable


def save_file(filename: str, content: str) -> None:
    """Ensure the directory exists and save content to a file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


async def process_question(question: str) -> dict:
    """Process a single question asynchronously."""
    q_input = CodeGenInput(
        question_payload=Question(question=question), # type: ignore
        initial_metadata=None,  # type: ignore
    )
    return await code_generator_v3.ainvoke(q_input)


async def main(q_list: list[str]) -> list[dict]:
    """Process a list of questions asynchronously."""
    tasks = [process_question(q) for q in q_list]
    return await asyncio.gather(*tasks)


def sanitize_filename(name: str) -> str:
    """Sanitize a string to be safe for use as a filename."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()


def save_question_outputs(results: list[dict], path_to_save: str) -> None:
    """Save the generated files for each question."""
    for idx, res in enumerate(results, 1):
        data = CodeGenOutput(**res)
        qtitle = data.metadata.get("title", "") or f"question_{idx}"
        safe_qtitle = sanitize_filename(qtitle)
        question_dir = os.path.join(path_to_save, safe_qtitle)
        os.makedirs(question_dir, exist_ok=True)

        files_to_save = {
            "question.html": getattr(data.files, "question_html", None),
            "solution.html": getattr(data.files, "solution_html", None),
            "server.js": getattr(data.files, "server_js", None),
            "server.py": getattr(data.files, "server_py", None),
            "info.json": json.dumps(data.metadata),
            "data.json": json.dumps(to_serializable(data)),
        }

        for fname, content in files_to_save.items():
            if content:
                save_file(os.path.join(question_dir, fname), content)


if __name__ == "__main__":
    q_list = [
        "A simply supported steel beam with a span of 4 meters carries a point load of 10 kN at its center. If the beam has a rectangular cross-section of width 100 mm and height 200 mm, what is the maximum bending stress in the beam? (Give your answer in MPa.)",
        # Add more questions as needed
    ]
    results = asyncio.run(main(q_list))
    # results: List[CodeGenOutput] 
    save_question_outputs(results, "./generated_question/")
