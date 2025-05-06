from fastapi import APIRouter, Depends, UploadFile, File, Form
from pydantic import BaseModel
from sqlmodel import Session
from typing import List, Tuple
import os
import shutil
import tempfile
from ast import literal_eval
from fastapi import Request
from typing import Optional
import json
from fastapi import FastAPI, HTTPException
import fitz  # PyMuPDF
from fitz import Page
from ..data.module import get_session
from ..data import question_models as service
from ..model.question_models import Package, QuestionFolder
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

import asyncio
from .utils import save_generated_module


router = APIRouter(prefix="/code_generator_chains")


class QuestionData(BaseModel):
    """
    Input model for the V1 text-based generator.
    Accepts a question and the name of the module to be created.
    """

    questions: List[str]
    package_name: str


def create_package_with_folders(
    package_title: str, question_packages: List[QuestionPackage], session: Session
):
    package = Package(title=package_title)
    session.add(package)
    session.commit()
    session.refresh(package)

    for q_pack in question_packages:
        if not isinstance(q_pack, QuestionPackage):
            q_pack = QuestionPackage(**q_pack)

        q_metadata: QuestionMetadata = q_pack.question_metadata
        q_files = q_pack.files
        initial_metadata: TextInitialMetadata = q_pack.initial_metadata

        folder = QuestionFolder(
            title=q_metadata.title,
            topic=q_metadata.topic,
            tags=q_metadata.tags,
            pre_reqs=q_metadata.prereqs,
            is_adaptive=literal_eval(q_metadata.isAdaptive),
            ai_generated=literal_eval(initial_metadata.ai_generated),
            reviewers=None,
            reviewed=False,
            created_by=initial_metadata.createdBy,
            package_id=package.id,
        )
        service.create_folder(folder, data=q_files, session=session)
    return package


@router.post("/v1", response_model=List[QuestionPackage])
async def generate_question_module_v1(
    data: QuestionData, session: Session = Depends(get_session)
) -> List[QuestionPackage]:
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

    tasks = []
    for question in data.questions:
        question_payload = QuestionPayload(
            question=question, solution_guide=None, additional_instructions=None
        )
        graph_input = QuestionPackage(
            question_payload=question_payload, initial_metadata=initial_metadata
        )
        tasks.append(graph.ainvoke(graph_input))

    question_packages: List[QuestionPackage] = await asyncio.gather(*tasks)
    create_package_with_folders(
        package_title=data.package_name,
        question_packages=question_packages,
        session=session,
    )
    return question_packages


@router.post("/v1/image_upload", response_model=ImageExtractionOutputState)
async def generate_question_module_image_v1(
    files: List[UploadFile] = File(...),
    folder_name: str = Form(...),
    session: Session = Depends(get_session),
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
            image_paths=temp_filepaths, initial_metadata=initial_metadata.model_dump()
        )

        result = await image_graph.ainvoke(graph_input)
        response = ImageExtractionOutputState(**result)

        q_packages = response.question_packages
        create_package_with_folders(
            package_title=folder_name, question_packages=q_packages, session=session
        )
    return response


# Define Version 2
from ..ai_workspace.lecture_processor.v2.lecture_processing_v2 import (
    graph as lecture_processor,
)
from ..ai_workspace.lecture_processor.v2.lecture_processing_v2 import (
    LectureMetadata,
    LectureOutputState,
    LectureInputState,
)


class LectureInput(BaseModel):
    seperate_image: Optional[bool] = False
    lecture_metadata: Optional[LectureMetadata] = None


@router.post("/v2/lecture_processor", response_model=LectureOutputState)
async def generate_lecture(request: Request, files: List[UploadFile] = File(...)):
    form_data = await request.form()
    data = LectureInputState(**form_data)
    try:
        temp_paths = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for file in files:
                # Handle PDF Uploads
                if file.content_type == "application/pdf":
                    pdf_doc = fitz.open(file)
                    pdf_name = data.lecture_metadata.lecture_title.replace(
                        " ", "_"
                    ) or os.path.splitext(os.path.basename(file))[0].replace(" ", "_")
                    page = pdf_doc.load_page(pgnum)

                    for pgnum in range(pdf_doc.page_count):

                        # Handle the case where we process the pages seperatly
                        ## Thus we annotate the page by annotating
                        if data.seperate_image:
                            # Get the page rectangle
                            rect = page.rect

                            # Calc width and height
                            ## Note: The coordinate system starts from the top right corner
                            width = rect.width
                            height = rect.height
                            # Get the right hand corder and create a circle
                            point = (width - 25, height - 25)
                            page.draw_circle(point, 25)
                            font_size = 30
                            point = fitz.Point(point[0], point[1])
                            page.insert_text(
                                point=point, text=str(pgnum), fontsize=font_size
                            )

                        page_name = f"{pdf_name}_page_{pgnum}.png"
                        temp_path = os.path.join(tmpdir, page_name)

                        # Conver to image
                        pix = page.get_pixmap()
                        pix.save(temp_path)
                        temp_paths.append(temp_path)

                        # Call the chain
                        graph_input = LectureInputState(
                            image_paths=temp_paths,
                            seperate_image=data.lecture_metadata,
                            lecture_metadata=data.lecture_metadata,
                        )
                        print("This is the graph input")

                        response = await lecture_processor.ainvoke(graph_input)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error data is not formatted correctly {e}"
        )

    return LectureOutputState(**response)
