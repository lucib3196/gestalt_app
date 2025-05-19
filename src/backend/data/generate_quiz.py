# data/generate_quiz_async.py
import os
import tempfile
import asyncio
import aiofiles
from backend.data.question_models import get_question_files
from ..data.helpers import read_file, format_question
from ..processing.code_runners.code_runner import run_generate
from typing import Literal
from ..processing.code_runners.utils import (
    CodeRunResponse,
    QuizData,
    GenerateQuizResponse,
)
import json
import ast


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
        get_question_files, question_folder_id, session=session
    )

    # Create a temporary directory for file operations.
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write file contents to the temporary directory asynchronously.
        for f in files:
            save_name = question_name_map.get(f.filename)
            filepath = os.path.join(tmpdir, save_name)

            if isinstance(f.content, bytes):
                f.content = f.content.decode("utf-8")

            async with aiofiles.open(filepath, "w", encoding="utf-8") as file:
                await file.write(f.content)

        # Check the question to see if it is adaptive
        metadata_file = os.path.join(tmpdir, "info.json")
        with open(metadata_file, "r") as f:
            meta = json.load(f)
            isAdaptive = meta.get("isAdaptive")

        # Conver to bool
        if isinstance(isAdaptive, str):
            isAdaptive = ast.literal_eval(isAdaptive)
        elif not isinstance(isAdaptive, bool):
            isAdaptive = False

        # Define data
        data = {}
        generated_data={}
        if isAdaptive == True:
            if server_type == "javascript":
                server_file = os.path.join(tmpdir, "server.js")
            else:
                server_file = os.path.join(tmpdir, "server.py")

            results: CodeRunResponse = await asyncio.to_thread(
                run_generate, server_file
            )
            # Catch an error
            if not results.success:
                return results  # This returns an object with the error code

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

        # Render the solution html
        solution_html_path = os.path.join(tmpdir, "solution.html")
        solution_content = await asyncio.to_thread(read_file, solution_html_path)
        if solution_content:
            rendered_solution = await asyncio.to_thread(
                format_question, html=solution_content, data=data
            )

        data = GenerateQuizResponse(
            question_html=rendered_question_html,
            quiz_data=generated_data,
            solution_html=rendered_solution if solution_content else None,
        )
        return CodeRunResponse(success=True, error=None, result=data)
