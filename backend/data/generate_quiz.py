# data/generate_quiz_async.py
import os
import tempfile
import asyncio
import aiofiles
from typing import Dict, Any
from .question_models import get_package_files
from ..data.helpers import read_file, format_question
from ..processing.code_runners.code_runner import run_generate

async def generate_quiz(module_id: int, session) -> str:
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
    files = await asyncio.to_thread(get_package_files, module_id=module_id, session=session)
    for f in files:
        # Set the save name based on the map.
        f.save_name = question_name_map.get(f.name, f.name)
    
    # Create a temporary directory for file operations.
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write file contents to the temporary directory asynchronously.
        for f in files:
            filepath = os.path.join(tmpdir, f.save_name)
            async with aiofiles.open(filepath, "w") as file:
                await file.write(f.content)
        
        # Run the generator file in a background thread.
        server_file = os.path.join(tmpdir, "server.js")
        generated_data = await asyncio.to_thread(run_generate, server_file)
        params = generated_data.get("params", {})
        correct_answers = generated_data.get("correct_answers", {})

        # Prepare the data payload for formatting.
        data = {
            "params": params,
            "correct_answers": correct_answers,
        }
        # Read the question HTML file asynchronously via a thread.
        question_html_path = os.path.join(tmpdir, "question.html")
        html_content = await asyncio.to_thread(read_file, question_html_path)
        # Format the question asynchronously in a thread.
        rendered_question_html = await asyncio.to_thread(format_question, html=html_content, data=data)
        return rendered_question_html
