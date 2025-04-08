import subprocess
import json5
import importlib.util
import os
from typing import Callable, Union, Any


def import_module_from_path(path: str) -> Any:
    """
    Dynamically imports a Python module from a given file path.

    Args:
        path (str): Path to the Python module.

    Returns:
        module: The imported module object.

    Raises:
        ImportError: If the module cannot be imported.
    """
    try:
        spec = importlib.util.spec_from_file_location("generate", path)
        if spec is None or spec.loader is None:
            raise ImportError("Could not load spec from path.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        raise ImportError(f"Error importing module from path '{path}': {e}")


def run_generate_py(path: str) -> dict:
    """
    Runs the 'generate' function from a Python module at the given path.

    Args:
        path (str): Path to the Python file containing a 'generate' function.

    Returns:
        dict: Output from the generate function.

    Raises:
        Exception: If importing or running the module fails.
    """
    try:
        module = import_module_from_path(path)
        if not hasattr(module, "generate"):
            raise AttributeError("The module does not have a 'generate' function.")
        return module.generate()
    except Exception as e:
        raise RuntimeError(f"Error running Python generator: {e}")


def run_js(path: str) -> dict[str, Union[str, dict[str, Any]]]:
    """
    Runs a Node.js script and parses the result as JSON.

    Args:
        path (str): Path to the JavaScript file with a generate() function.

    Returns:
        dict: Parsed JSON output from the JS file.

    Raises:
        RuntimeError: If the script fails to run or returns invalid JSON.
    """
    try:
        result = subprocess.run(
            ["node", path, "generate"],
            capture_output=True,
            text=True,
            check=True
        )
        return json5.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"JavaScript execution failed: {e.stderr or e.stdout}")
    except Exception as e:
        raise RuntimeError(f"Error running JS file '{path}': {e}")


def run_generate(path: str) -> Union[dict, tuple[dict, int]]:
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
        return {"error": "File not found"}, 404

    base_name = os.path.basename(path)

    try:
        if base_name in generators:
            return generators[base_name](path)
        else:
            return {"error": f"Unsupported file type: {base_name}"}, 400
    except Exception as e:
        return {"error": str(e)}, 400


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
