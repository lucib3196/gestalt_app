# data/generate_quiz.py
import os
import tempfile
from typing import Dict, Any
from ..data.crud import get_module_files
from ..data.helpers import read_file, format_question
from ..processing.code_runners.code_runner import run_generate

def generate_quiz(module_id: int, session) -> None:
    """
    Generates a quiz for a given module.

    This function retrieves file records for a module, writes them to a temporary
    directory, runs the generator file, and then formats the HTML question.
    
    Args:
        module_id (int): Module identifier.
        session: The database session.
    
    Raises:
        ValueError: If the required question file is missing.
    """
    question_name_map = {
        "question_txt": "question.txt",
        "question_html": "question.html",
        "server_js": "server.js",
        "server_py": "server.py",
        "solution_html": "solution.html",
        "metadata": "info.json",
    }
    # Retrieve files associated with the module.
    files = get_module_files(module_id=module_id, session=session)
    for f in files:
        # Set the save name based on the map.
        f.save_name = question_name_map.get(f.name, f.name)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write file contents to the temporary directory.
        for f in files:
            filepath = os.path.join(tmpdir, f.save_name)
            with open(filepath, "w") as file:
                file.write(f.content)
        
        # Run the generator file.
        server_file = os.path.join(tmpdir, "server.js")
        generated_data = run_generate(server_file)
        params = generated_data.get("params", {})
        correct_answers = generated_data.get("correct_answers", {})

        data = {
            "params": params,
            "correct_answers": correct_answers,
        }
        question_html_path = os.path.join(tmpdir, "question.html")
        html_content = read_file(question_html_path)
        rendered_question_html = format_question(html=html_content, data=data)
        return rendered_question_html
