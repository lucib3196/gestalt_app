from ..models.questionModels import FilesData
from ..models.tokenCounter import StepTokenUsage
from typing import Any, List


def merge_files_data(existing: "FilesData", new: "FilesData") -> "FilesData":
    """
    Merges two FilesData instances by taking non-empty fields from the new value.
    """
    return FilesData(
        question_html=new.question_html or existing.question_html,
        server_js=new.server_js or existing.server_js,
        server_py=new.server_py or existing.server_py,
        solution_html=new.solution_html or existing.solution_html,
        metadata=new.metadata or existing.metadata,
    )


def keep_first(existing: Any, new: Any) -> Any:
    return existing or new


def reduce_token_usage(
    existing: List[StepTokenUsage], new: List[StepTokenUsage]
) -> List[StepTokenUsage]:
    seen = {tu.step_name for tu in existing}
    return existing + [tu for tu in new if tu.step_name not in seen]
