# data/generate_quiz_async.py
import os
import tempfile
import asyncio
import aiofiles
from .question_models import get_folder_files
from ..data.helpers import read_file, format_question
from ..processing.code_runners.code_runner import run_generate
from typing import Literal
from ..processing.code_runners.utils import (
    CodeRunResponse,
    QuizData,
    GenerateQuizResponse,
)


async def generate_quiz(
    question_folder_id: int,
    session,
    server_type: Literal["javascript", "python"] = "javascript",
) -> CodeRunResponse:
    """
    Asynchronously generates a quiz for a given module.

    This function retrieves file records for a module, writes them to a temporary
    directory asynchronously, runs the generator file in a thread (since it is blocking),
    and then formats the HTML question.

    Args:
        module_id (int): Module identifier.
        session: The database session.

    Returns:
        str: The rendered HTML for the quiz question.

    Raises:
        ValueError: If the required question file is missing.
    """
    # Mapping from file type keys to file names.
    question_name_map = {
        "question_txt": "question.txt",
        "question_html": "question.html",
        "server_js": "server.js",
        "server_py": "server.py",
        "solution_html": "solution.html",
        "metadata": "info.json",
    }
    # Retrieve files associated with the module in a thread to avoid blocking.
    files = await asyncio.to_thread(
        get_folder_files, question_folder_id, session=session
    )
    for f in files:
        # Set the save name based on the map.
        f.save_name = question_name_map.get(f.name)

    # Create a temporary directory for file operations.
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write file contents to the temporary directory asynchronously.
        for f in files:
            filepath = os.path.join(tmpdir, f.save_name)

            if isinstance(f.content, bytes):
                f.content = f.content.decode("utf-8")

            async with aiofiles.open(filepath, "w", encoding="utf-8") as file:
                await file.write(f.content)

        # Run the generator file in a background thread.
        if server_type == "javascript":
            server_file = os.path.join(tmpdir, "server.js")
        else:
            server_file = os.path.join(tmpdir, "server.py")

        results: CodeRunResponse = await asyncio.to_thread(run_generate, server_file)
        print("This is the result", results)

        # Catch an error
        if not results.success:
            return results

        generated_data: QuizData = results.result
        params = generated_data.params
        correct_answers = generated_data.correct_answers
        data = {"params": params, "correct_answers": correct_answers}

        # Read the question HTML file asynchronously via a thread.
        question_html_path = os.path.join(tmpdir, "question.html")
        html_content = await asyncio.to_thread(read_file, question_html_path)
        # Format the question asynchronously in a thread.
        rendered_question_html = await asyncio.to_thread(
            format_question, html=html_content, data=data
        )
        data = GenerateQuizResponse(
            question_html=rendered_question_html, quiz_data=generated_data
        )
        return CodeRunResponse(success=True, error=None, result=data)
