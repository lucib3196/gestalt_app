import subprocess
import json5
from pydantic import ValidationError
from .response_models import CodeRunResponse, QuizData
import json


def run_js(path: str) -> CodeRunResponse:
    """
    Runs a Node.js script and parses the result as a QuizData object.
    Provides fallback if output is malformed or validation fails.
    """
    try:
        result = subprocess.run(
            ["node", path, "generate"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        print("This is the stdout")
        print(stdout)
        if result.returncode != 0:
            return CodeRunResponse(
                success=False,
                error=f"JavaScript script returned an error:\n{stderr}",
                result=None,
                http_status_code=500,
            )

        if not stdout:
            return CodeRunResponse(
                success=False,
                error="No output was returned from the JavaScript script.",
                result=None,
                http_status_code=500,
            )

        try:
            parsed = json5.loads(stdout)
            # If parsed is a stringified JSON, parse it again
            if isinstance(parsed, str):
                parsed = json5.loads(parsed)

            # Validate structure before model instantiation
            required_keys = {"params", "correct_answers", "nDigits", "sigfigs"}
            if not isinstance(parsed, dict) or not required_keys.issubset(parsed):
                parsed_keys = parsed.keys() if isinstance(parsed, dict) else type(parsed).__name__
                raise ValueError(f"Missing required keys: expected {required_keys}, got {parsed_keys}")

            quiz_data = QuizData(**parsed)

            return CodeRunResponse(
                success=True,
                error=None,
                result=quiz_data,
                http_status_code=200,
            )

        except (json.JSONDecodeError, ValidationError, ValueError) as parse_err:
            return CodeRunResponse(
                success=False,
                error=f"Parsing, structure, or validation error:\n{parse_err}",
                result=stdout if not isinstance(parse_err, ValidationError) else parsed,
                http_status_code=400 if not isinstance(parse_err, ValidationError) else 422,
            )

    except subprocess.TimeoutExpired:
        return CodeRunResponse(
            success=False,
            error="JavaScript script execution timed out.",
            result=None,
            http_status_code=504,
        )

    except Exception as e:
        return CodeRunResponse(
            success=False,
            error=f"Unexpected error running JavaScript file '{path}':\n{e}",
            result=None,
            http_status_code=500,
        )



def test():
    path = r"backend\processing\code_runners\test.js"
    print(run_js(path))


if __name__ == "__main__":
    test()
