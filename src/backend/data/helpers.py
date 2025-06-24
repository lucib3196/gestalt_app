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


def sanitize_for_template(data: dict) -> dict:
    """
    Recursively convert all primitive values (str, int, float, bool) into strings.
    This ensures no unintentional braces or backslashes break LaTeX/Jinja parsing.
    """
    safe = {}
    for key, val in data.items():
        if isinstance(val, dict):
            safe[key] = sanitize_for_template(val)
        elif isinstance(val, (str, int, float, bool)):
            safe[key] = str(val)
        else:
            safe[key] = val  # leave complex objects as-is, or convert as needed
    return safe


# This will propably need to be moved eventually
from collections import defaultdict
from jinja2 import Environment
from jinja2 import Environment


def format_question(html: str, data: dict) -> str:
    """
    Processes and renders an HTML question template that now uses
    the new `[[ … ]]` placeholder syntax instead of `{{ … }}`.

    Args:
        html (str): The raw HTML template content.
        data (dict): Data for rendering (must include a "params" key).

    Returns:
        str: The rendered HTML with placeholders resolved.
    """
    # ── 1. Pre-process the HTML (e.g., custom tag replacement) ──────────────────
    processed_html = process(html)  # Your existing tag-replacement logic
    print("[format_question] Processed HTML after tag replacement:")
    print(processed_html)

    # ── 2. Sanitize the data going into the template ────────────────────────────
    safe_data = sanitize_for_template(data)
    print("[format_question] Data after sanitization:")
    print(safe_data)

    # ── 3. Render with Jinja2 configured for [[ … ]] placeholders ──────────────
    env = Environment(
        autoescape=True,
        variable_start_string="[[",  # NEW delimiter start
        variable_end_string="]]",  # NEW delimiter end
        # (block/comment delimiters remain the Jinja defaults)
    )

    template = env.from_string(processed_html)
    print("[format_question] Jinja2 Template object created with [[…]] delimiters.")

    rendered = template.render(**safe_data)
    print(rendered)
    print("[format_question] Rendering complete.")

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
