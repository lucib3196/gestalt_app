# data/helpers.py
import os
from typing import List
from jinja2 import Template
from ..processing.pl_utils.process_prairielearn import process
import zipfile
import io


def file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return os.path.exists(file_path)


def read_file(file_path: str) -> str:
    """Read the entire contents of a file."""
    if not file_exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")
    with open(file_path, "r") as file:
        return file.read()


# This will propably need to be moved eventually
def format_question(html: str, data: dict) -> str:
    """
    Processes and renders an HTML question template with provided data.

    Args:
        html (str): The HTML template content.
        data (dict): Data for rendering, expects a "params" key.

    Returns:
        str: The rendered HTML.
    """
    # Apply any preprocessing if needed.
    processed_html = process(html)

    template = Template(processed_html)

    rendered = template.render(params=data.get("params", {}))
    return rendered


def create_zip_file(file_paths: List[str]) -> io.BytesIO:
    """
    Creates an in-memory ZIP file from the list of file paths, storing only the basename of each file in the archive.

    Args:
        file_paths (List[str]): A list of file paths to include in the ZIP archive.

    Returns:
        io.BytesIO: A BytesIO object containing the ZIP file data.
    """
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zipf:
        for f_path in file_paths:
            zipf.write(f_path, arcname=os.path.basename(f_path))
    memory_file.seek(0)
    return memory_file
