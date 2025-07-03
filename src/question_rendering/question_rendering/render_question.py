from pathlib import Path
from typing import Union, Literal, Optional
import json
import os
import shutil  # NEW
from jinja2 import Environment
from typing import Any

from question_rendering.code_runner import run_generate
from question_rendering.models import QuizData, QuizResponse, CodeRunResponse
from question_rendering.html_tag_processing.process_tags import apply_all_replacers
from pydantic import BaseModel
from question_rendering.utils.math_helpers import round_value, Number

# --------------------------------------------------------------------------- #
#  Constants
# --------------------------------------------------------------------------- #

STYLES_PATH = Path(r"gestalt\styles\QuestionStyles.css")

MATHJAX_HEADER = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Rendered Question</title>

  <!-- External CSS for question styling -->
  {styles_link}

  <!-- MathJax v3 configuration -->
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$']],      // $ … $
        displayMath: [['$$', '$$']]    // $$ … $$
      }}
    }};
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
          id="MathJax-script" async></script>

  <style>
    body {{ margin: 2rem auto; max-width: 800px; font-family: sans-serif; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #


def _wrap_with_mathjax(body_html: str, *, stylesheet: Path | None = STYLES_PATH) -> str:
    """
    Embed `body_html` inside a minimal MathJax-enabled HTML shell.
    If `stylesheet` is supplied, its path is inserted as <link rel="stylesheet">.
    """
    styles_link = ""
    if stylesheet:
        href = stylesheet.as_posix()  # keeps forward slashes
        styles_link = f'<link rel="stylesheet" href="{href}">'
    return MATHJAX_HEADER.format(body=body_html, styles_link=styles_link)


def sanitize_for_template(data: dict) -> dict:
    """Recursively coerce nested dict values to str so Jinja can handle them."""
    safe: dict[str, str] = {}
    for key, val in data.items():
        if isinstance(val, dict):
            safe[key] = sanitize_for_template(val)  # type: ignore
        elif isinstance(val, (str, int, float, bool)):
            safe[key] = str(val)
        else:
            safe[key] = val
    return safe


def is_adaptive_question(metadata_file: Path) -> bool:
    """Return True if info.json declares `"isAdaptive": true`."""
    if not metadata_file.exists():
        return False
    try:
        metadata_content: dict = json.loads(metadata_file.read_text("utf-8"))
        is_adaptive = metadata_content.get("isAdaptive", False)
        if isinstance(is_adaptive, str):
            is_adaptive = is_adaptive.strip().lower() == "true"
        return bool(is_adaptive)
    except Exception:
        return False


# Needs a better method but should work for now
def round_generated_values(values: dict[str, Any], digits):
    for key, value in values.items():
        if isinstance(value, Number):
            values[key] = round_value(value, digits=digits)
    return values


def run_adaptive_generate(
    path_obj: Path, server_type: Literal["javascript", "python"]
) -> Union[QuizData, CodeRunResponse]:
    """Run server.(js|py) to obtain adaptive QuizData."""
    server_file = path_obj / (
        "server.js" if server_type == "javascript" else "server.py"
    )
    try:
        results: CodeRunResponse = run_generate(server_file)
        if not results.success or results.quiz_response is None:
            return results

        # Process things such as roudning

        results.quiz_response.params = round_generated_values(
            results.quiz_response.params, results.quiz_response.nDigits
        )
        results.quiz_response.correct_answers = round_generated_values(
            results.quiz_response.correct_answers, results.quiz_response.nDigits
        )
        print(results.quiz_response)
        return results.quiz_response
    except Exception as e:
        return CodeRunResponse(
            success=False,
            error=f"Could not run adaptive generate: {e}",
            quiz_response=None,
        )


def render_adaptive_question(html: str, quiz_data: QuizData) -> str:
    print("Inside")
    print(quiz_data)
    processed_html = apply_all_replacers(html)
    quiz_data_dict = (
        quiz_data.dict()
        if hasattr(quiz_data, "dict")
        else dict(quiz_data.__dict__)  # type: ignore[attr-defined]
    )
    quiz_data_safe = sanitize_for_template(quiz_data_dict)
    print("safe")
    print(quiz_data)

    env = Environment(
        autoescape=True, variable_start_string="[[", variable_end_string="]]"
    )
    template = env.from_string(
        str(processed_html)
        .replace(r"\(", "$")
        .replace(r"\)", "$")
        .replace(r"\[", "$$")
        .replace(r"\]", "$$")
    )
    print(template)
    return template.render(**quiz_data_safe)


def render_non_adaptive_question(html: str) -> str:
    processed_html = apply_all_replacers(html)
    env = Environment(
        autoescape=True, variable_start_string="[[", variable_end_string="]]"
    )
    template = env.from_string(
        str(processed_html)
        .replace(r"\(", "$")
        .replace(r"\)", "$")
        .replace(r"\[", "$$")
        .replace(r"\]", "$$")
    )
    return template.render()


class RenderedQuestion(BaseModel):
    question_html: str
    solution_html: str
    quiz_data: Optional[QuizData] = None


# --------------------------------------------------------------------------- #
#  Main entrypoint
# --------------------------------------------------------------------------- #


def render_question(
    path: Union[str, Path],
    server_type: Literal["javascript", "python"],
    local_dir: bool = False,
) -> Union[RenderedQuestion, CodeRunResponse]:
    """
    Render question HTML (and solution, if any).
    If `local_dir=True`, write HTML + CSS copies into `<question>/output/`.
    """
    path_obj = Path(path).expanduser().resolve()
    metadata_file = path_obj / "info.json"
    html_file = path_obj / "question.html"
    solution_file = path_obj / "solution.html"

    is_adaptive_flag = is_adaptive_question(metadata_file)

    question_html = ""
    solution_html = ""
    quiz_data: Optional[QuizData | CodeRunResponse] = None

    try:
        if is_adaptive_flag:
            quiz_data = run_adaptive_generate(path_obj, server_type)
            # At this point in the code logid if the the instance is a code run response there is an error
            if isinstance(quiz_data, CodeRunResponse) and not quiz_data.success:
                return quiz_data
            else:
                question_html = render_adaptive_question(html_file.read_text(errors="replace", encoding="utf-8"), quiz_data)  # type: ignore[arg-type]
                if solution_file.exists():
                    solution_html = render_adaptive_question(solution_file.read_text(errors="replace", encoding="utf-8"), quiz_data)  # type: ignore[arg-type]
        else:
            question_html = render_non_adaptive_question(html_file.read_text())
            if solution_file.exists():
                solution_html = render_non_adaptive_question(solution_file.read_text())
    except Exception as e:
        return CodeRunResponse(
            success=False,
            error=f"Unknown Error {e}",
            quiz_response=None,
            http_status_code=500,
        )

    rendered = RenderedQuestion(
        question_html=question_html,
        solution_html=solution_html,
        quiz_data=quiz_data if isinstance(quiz_data, QuizData) else None,
    )

    # ----------------------------------------------------------------------- #
    #  Local output (HTML + copied CSS)
    # ----------------------------------------------------------------------- #
    if local_dir:
        output_dir = path_obj / "output"
        try:
            output_dir.mkdir(exist_ok=True)

            # Copy stylesheet into the same output directory
            local_stylesheet = output_dir / STYLES_PATH.name
            try:
                shutil.copy2(STYLES_PATH, local_stylesheet)
            except Exception as css_err:
                print(f"[render_question] Could not copy stylesheet: {css_err}")

            # Wrap HTML, linking to the **local** copy of the stylesheet
            q_html_wrapped = _wrap_with_mathjax(
                rendered.question_html, stylesheet=Path(STYLES_PATH.name)
            )
            s_html_wrapped = _wrap_with_mathjax(
                rendered.solution_html, stylesheet=Path(STYLES_PATH.name)
            )

            (output_dir / "question_output.html").write_text(
                q_html_wrapped, encoding="utf-8"
            )
            (output_dir / "solution_output.html").write_text(
                s_html_wrapped, encoding="utf-8"
            )
        except Exception as e:
            print(f"[render_question] Failed to write output files: {e}")

    return rendered


# --------------------------------------------------------------------------- #
#  CLI / manual test
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    path = r"generated_question\MaximumBendingStressInBeam"
    render_question(path, "javascript", local_dir=True)
