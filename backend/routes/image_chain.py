import os
import shutil
import tempfile
from typing import List, Tuple

from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session

from ..ai_workspace.agents.engineering_codegen.code_generator_image import (
    graph,
    ImageInputState,
    ImageExtractionOutputState,
    InitialMetadata
)
from ..data import question_models as service
from ..model.question_models import Package
from ..data.module import get_session

router = APIRouter(prefix="/chain_image")


@router.post("/preview", response_model=ImageExtractionOutputState)
async def preview_extracted_content(files: List[UploadFile]):
    """
    Process uploaded image files using the AI pipeline and return the raw output,
    without saving anything to the database.

    Used for previewing what the extracted content will look like.
    """
    temp_filepaths = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            temp_path = os.path.join(tmpdir, file.filename)
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            temp_filepaths.append(temp_path)

        graph_input = ImageInputState(image_paths=temp_filepaths)
        response = await graph.ainvoke(graph_input)

    return response


@router.post("/extract-and-save", response_model=ImageExtractionOutputState)
async def extract_and_save_content(
    files: List[UploadFile],
    session: Session = Depends(get_session)
):
    """
    Process uploaded image files using the AI pipeline and save the resulting
    content (questions and files) into the database as a module.
    """
    initial_metadata = InitialMetadata(
        createdBy="lberm007@ucr.edu",
        qtype="num",
        nSteps="1",
        updatedBy="",
        ai_generated="True",
        reviewed="False",
        codelang="JavaScript"
    )

    temp_filepaths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            temp_path = os.path.join(tmpdir, file.filename)
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            temp_filepaths.append(temp_path)

        graph_input = ImageInputState(
            image_paths=temp_filepaths,
            initial_metadata=initial_metadata.model_dump()
        )
        response = await graph.ainvoke(graph_input)

        question_packages = response.get("question_packages", [])
        folders = []
        for q_pack in question_packages:
            q_pack = q_pack.model_dump()
            q_files = q_pack.get("files", {})
            question_title = q_pack.get("question_metadata", {}).get("title", "Untitled")
            folders.append((question_title, q_files))

        await save_generated_module(folders, title="Module", session=session)

    return response


async def save_generated_module(
    folders: List[Tuple[str, dict[str, str]]],
    title: str = "Module",
    session: Session = Depends(get_session)
):
    """
    Save AI-generated folders and files into the database as a new module.
    """
    module = Package(title=title)
    return service.create_module_with_folders(module, folders=folders, session=session)
