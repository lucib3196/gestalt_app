import subprocess
import json5
from .utils import CodeRunResponse, QuizData


def run_js(path: str) -> CodeRunResponse:
    """
    Runs a Node.js script and parses the result as JSON.

    Args:
        path (str): Path to the JavaScript file.

    Returns:
        Response: success status, result or error message.
    """
    try:
        result = subprocess.run(
            ["node", path, "generate"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        # Handle subprocess-level error
        if result.returncode != 0:
            return CodeRunResponse(
                success=False,
                error=result.stderr.strip() or "JavaScript script returned an error.",
                result=None,
                status_code=500,
            )

        # Handle empty stdout
        if not result.stdout.strip():
            return CodeRunResponse(
                success=False,
                error="No output returned from JavaScript script.",
                result=None,
                status_code=500,
            )

        # Attempt to parse stdout as JSON
        try:
            parsed = json5.loads(result.stdout)
            print(parsed)
        except Exception as parse_err:
            return CodeRunResponse(
                success=False,
                error=f"Failed to parse JSON5: {parse_err}",
                result=result.stdout.strip(),
                status_code=500,
            )

        return CodeRunResponse(
            success=True,
            error=None,
            result=QuizData(
                **parsed
            ),
            status_code=200,
        )

    except subprocess.TimeoutExpired:
        return CodeRunResponse(
            success=False,
            error="JavaScript execution timed out.",
            result=None,
            status_code=500,
        )

    except Exception as e:
        return CodeRunResponse(
            success=False,
            error=f"Unexpected error running JS file '{path}': {e}",
            result=None,
            status_code=500,
        )


def test():
    path = r"backend\processing\code_runners\test.js"
    print(run_js(path))


if __name__ == "__main__":
    test()
