import os
from .utils import CodeRunResponse
from typing import Callable
from .run_js import run_js
from .run_py import run_generate_py


def run_generate(path: str) -> CodeRunResponse:
    """
    Dispatches to either a Python or JavaScript generator based on the file extension.

    Args:
        path (str): Path to the generator file.

    Returns:
        dict | tuple: The output from the generator or an error tuple.
    """
    generators: dict[str, Callable[[str], dict]] = {
        "server.js": run_js,
        "server.py": run_generate_py,
    }
    if not os.path.isfile(path):
        return CodeRunResponse(
            success=False, error="File not Found", result=None, status_code=404
        )

    base_name = os.path.basename(path)

    try:
        if base_name in generators:
            return generators[base_name](
                path
            )  # This returns a CodeRun response already for us.
        else:
            return CodeRunResponse(
                success=False,
                error=f"Unsupported file type: {base_name}",
                result=None,
                status_code=404,
            )

    except Exception as e:
        return CodeRunResponse(
            success=False, error=f"Error E: {e}", result=None, status_code=404
        )


if __name__ == "__main__":
    js_path = r"backend/processing/code_runners/test.js"
    py_path = r"backend/processing/code_runners/test.py"

    try:
        print("JS Output:")
        print(run_js(js_path))
    except Exception as e:
        print(f"JS Error: {e}")

    try:
        print("\nPython Output:")
        print(run_generate_py(py_path))
    except Exception as e:
        print(f"Python Error: {e}")
