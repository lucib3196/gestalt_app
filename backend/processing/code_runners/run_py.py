from typing import Any
import importlib.util

from .utils import CodeRunResponse, QuizData


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


def run_generate_py(path: str) -> CodeRunResponse:
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
        data = module.generate()
        if "params" and "correct_answers" in data.keys():
            data = QuizData(**data)
            return CodeRunResponse(
                success=True, error=None, result=data, http_status_code=202
            )
        else:
            return CodeRunResponse(
                success=False,
                error="Key Error params or correct answers not found in generated data",
                result=None,
                http_status_code=500,
            )

    except Exception as e:
        return CodeRunResponse(
            success=False,
            error=f"Error running Python generator: {e}",
            result=None,
            http_status_code=500,
        )


def test():
    path = r"backend\processing\code_runners\test.py"
    print(run_generate_py(path))


if __name__ == "__main__":
    test()
