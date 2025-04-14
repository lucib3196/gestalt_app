from fastapi import APIRouter, Depends, UploadFile, File, Form
from pydantic import BaseModel
from sqlmodel import Session
from typing import List, Tuple
import os
import shutil
import tempfile

from ..data.module import get_session
from ..data import crud as service
from ..model.module_db import ModuleSimple
from ..ai_workspace.agents.engineering_codegen.code_generator import (
    QuestionPayload,
    InitialMetadata as TextInitialMetadata,
    QuestionPackage,
    FilesData,
    QuestionMetadata,
    compiled_graph as graph,
)
from ..ai_workspace.agents.engineering_codegen.code_generator_image import (
    ImageInputState,
    ImageExtractionOutputState,
    InitialMetadata as ImageInitialMetadata,
    graph as image_graph,
)
from .utils import save_generated_module


router = APIRouter(prefix="/code_generator_chains/v1")


class QuestionData(BaseModel):
    """
    Input model for the V1 text-based generator.
    Accepts a question and the name of the module to be created.
    """
    question: str
    folder_name: str


@router.post("/", response_model=QuestionPackage)
async def generate_question_module_v1(
    data: QuestionData, session: Session = Depends(get_session)
) -> QuestionPackage:
    """
    Version 1 endpoint for generating a question module from text input using the code generation graph.
    """

    initial_metadata = TextInitialMetadata(
        createdBy="lberm007@ucr.edu",
        qtype="num",
        nSteps=1,
        updatedBy="",
        codelang="JavaScript",
        reviewed="False",
        ai_generated="True",
    )
    
    
    
    question_payload = QuestionPayload(
        question=data.question,
        solution_guide=None,
        additional_instructions=None,
    )

    graph_input = QuestionPackage(
        question_payload=question_payload,
        initial_metadata=initial_metadata,
    )

    response_data = await graph.ainvoke(graph_input)
    response = QuestionPackage(**response_data)

    question_title = response.question_metadata.title
    question_files = response.files
    module_content = [(question_title, question_files)]

    await save_generated_module(
        folders=module_content,
        title=data.folder_name,
        session=session
    )

    return response


@router.post("/image_upload", response_model=ImageExtractionOutputState)
async def generate_question_module_image_v1(
    files: List[UploadFile] = File(...),
    folder_name: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Endpoint to process uploaded image files using the AI pipeline
    and save the generated module to the database.
    """
    initial_metadata = ImageInitialMetadata(
        createdBy="lberm007@ucr.edu",
        qtype="num",
        nSteps=1,
        updatedBy="",
        codelang="JavaScript",
        reviewed="False",
        ai_generated="True",
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

        result = await image_graph.ainvoke(graph_input)
        response = ImageExtractionOutputState(**result)

        folders = []
        for q_pack in response.question_packages:
            q_files = q_pack.files
            question_title = q_pack.question_metadata.title or "Untitled"
            folders.append((question_title, q_files))

        await save_generated_module(folders, title=folder_name, session=session)

    return response
