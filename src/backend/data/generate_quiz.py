# data/generate_quiz_async.py
import os
import tempfile
import asyncio
import aiofiles
from backend.data.question_models import get_question_files
from backend.data.helpers import read_file, format_question
from question_rendering import RenderedQuestion, render_question, CodeRunResponse
from ..processing.code_runners.code_runner import run_generate
from typing import Literal, Union
from pathlib import Path
from ..processing.code_runners.response_models import (
    QuizData,
    GenerateQuizResponse,
)
import json
import shutil


async def generate_quiz(
    question_folder_id: int,
    session,
    server_type: Literal["javascript", "python"] = "javascript",
) -> Union[CodeRunResponse, RenderedQuestion]:
    """
    Download all files for a question bundle, run `render_question`, and
    clean up the temporary directory automatically.

    Heavy blocking I/O (disk + CPU-bound render) is off-loaded to threads so
    the event loop stays responsive.
    """
    files = await asyncio.to_thread(get_question_files, question_folder_id, session)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)  # convenience

        async def _write_file(file_obj) -> None:
            dest = tmp_path / file_obj.filename
            data = file_obj.content
            if isinstance(data, bytes):
                try:
                    data = data.decode("utf-8")
                except UnicodeDecodeError:
                    async with aiofiles.open(dest, "w") as fh:
                        await fh.write(file_obj.content)
                    return

            async with aiofiles.open(dest, "w") as fh:
                await fh.write(data)

        await asyncio.gather(*[_write_file(f) for f in files])

        result = await asyncio.to_thread(render_question, tmp_path, server_type)

        if isinstance(result, (CodeRunResponse, RenderedQuestion)):
            return result
        raise ValueError("render_question returned an unexpected type")


