# data/helpers.py
import os
from jinja2 import Template
from ..processing.pl_utils.process_prairielearn import process

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
