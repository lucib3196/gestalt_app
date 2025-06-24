import os
import json
import asyncio
from typing import List, Optional

from ai_workspace.agentsv2.image_codegenerator.agent import (
    compiled_graph,
    StateInput,
    StateOutput,
)
from ai_workspace.agentsv2.code_generator.ver3.code_generator import (
    CodeGenInput,
    CodeGenOutput,
)
from schemas import Question
from ai_workspace.utils import to_serializable


def save_file(filename: str, content: str) -> None:
    """Ensure the directory exists and save content to a file."""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error saving file {filename}: {e}")


def sanitize_filename(name: str) -> str:
    """Sanitize a string to be safe for use as a filename."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()


async def process(
    image_paths: List[str], initial_metadata: Optional[dict] = None
) -> List[CodeGenOutput]:
    """Process the input images and return the generated code outputs."""
    print(image_paths)
    input_q = StateInput(image_paths=image_paths, initial_metadata=initial_metadata)
    # Await the asynchronous task to process the input query
    results = await compiled_graph.ainvoke(input_q)
    return results


def save_question_outputs(results: list[dict], path_to_save: str) -> None:
    """Save the generated files for each question."""
    for idx, data in enumerate(results, 1):
        data = CodeGenOutput(**data)
        qtitle = data.metadata.get("title", "") or f"question_{idx}"
        safe_qtitle = sanitize_filename(qtitle)
        question_dir = os.path.join(path_to_save, safe_qtitle)
        os.makedirs(question_dir, exist_ok=True)

        files_to_save = {
            "question.html": getattr(data.files, "question_html", None),
            "solution.html": getattr(data.files, "solution_html", None),
            "server.js": getattr(data.files, "server_js", None),
            "server.py": getattr(data.files, "server_py", None),
            "info.json": json.dumps(data.metadata, indent=2),
            "data.json": json.dumps(to_serializable(data), indent=2),
        }

        for fname, content in files_to_save.items():
            if content:
                save_file(os.path.join(question_dir, fname), content)


if __name__ == "__main__":
    image_paths = [r"..\Images\handwritten\mass_block.png"]
    initial_metadata = None

    # Run the process function asynchronously
    results = asyncio.run(process(image_paths, initial_metadata=initial_metadata))
    print(results)
    output = results.get("output", {})
    print(output)
    save_question_outputs(output, "./generated_question/")
