# Standard library
import os
import tempfile
from datetime import date, datetime
import asyncio

# Third-party libraries
import fitz
from fitz import Page
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlmodel import Session
from typing import Optional, List, Union
from ast import literal_eval

# Internal modules
from backend.model.question_models import (
    QuestionFolder,
    Package,
    File as IndividualFile,
)
from backend.data.module import get_session

# Modesl for AI gen
from ai_workspace.models.questionModels import InitialMetadata, Question

# Code Generator Input
from ai_workspace.code_generator.v2.code_generator import (
    CodeGenInput,
    CodeGenState,
    compiled_graph as codegen_graph,
)
from ai_workspace.lecture_processor.v2.lecture_processing_v2 import (
    LectureInputState,
    LectureOutputState,
    to_serializable,
    LectureMetadata,
    graph as lecture_processor,
)
from backend.data import question_models as service

# Fast API Set Up
router = APIRouter(prefix="/codegen_v2")
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "application/pdf"}


# Input Schema
class QuestionData(BaseModel):
    """
    Input model for the V2 text-based generator.
    Accepts a question and the name of the module to be created.
    """

    questions: List[str]
    package_name: str


# Initial Metadata Should Be Changed

initial_metadata = InitialMetadata(
    createdBy="lberm007@ucr.edu",
    qtype="num",
    nSteps=1,
    updatedBy="",
    codelang="JavaScript",
    reviewed="False",
    ai_generated="True",
)


@router.post("/text", response_model=List[CodeGenState])
async def gen_question_text_v2(
    data: QuestionData,
    session: Session = Depends(get_session),
):
    # 1) Kick off all codegen tasks in parallel
    tasks = [
        codegen_graph.ainvoke(
            CodeGenInput(
                question_payload=Question(question=q),
                question_metadata=initial_metadata,
            )
        )
        for q in data.questions
    ]
    question_packages: List[CodeGenState] = await asyncio.gather(*tasks)

    # 2) Create top-level package
    package = Package(name=data.package_name)
    session.add(package)
    session.commit()
    session.refresh(package)

    # Create the folders
    created_folders = service.create_question_pack_v2(
        package=package, qpacks=question_packages, session=session
    )
    return question_packages


@router.post("/process_lecture", response_model=LectureOutputState)
async def process_lecture(
    lecture_title: str = Form(...),
    course_name: str = Form(...),
    course_code: Union[str, int] = Form(...),
    instructor_name: str = Form(...),
    lecture_date: Optional[date] = Form(None),
    semester: str = Form(...),
    seperate_image: Optional[bool] = Form(False),
    file: List[UploadFile] = File(...),
    session: Session = Depends(get_session),
):
    def print_db_status(entity, name: str):
        print(f"[DB] {name} - ID: {getattr(entity, 'id', None)} | {entity}")

    try:
        print("[INFO] Packing lecture metadata...")
        metadata = LectureMetadata(
            lecture_title=lecture_title,
            course_name=course_name,
            course_code=course_code,
            instructor_name=instructor_name,
            lecture_date=lecture_date,
            semester=semester,
            seperate_image=seperate_image,
        )

        temp_filepaths = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for f in file:
                print(f"[INFO] Processing file: {f.filename} ({f.content_type})")
                if f.content_type not in ALLOWED_MIME_TYPES:
                    detail = f"{'_'.join(list(ALLOWED_MIME_TYPES))}"
                    print(f"[ERROR] File type {f.content_type} not allowed.")
                    raise HTTPException(status_code=404, detail=detail)
                temp_path = os.path.join(tmpdir, f.filename)
                with open(temp_path, "wb") as buffer:
                    contents = await f.read()
                    buffer.write(contents)
                print(f"[INFO] Saved file to temp path: {temp_path}")

                mime = f.content_type
                match mime:
                    case "application/pdf":
                        print("[INFO] Found PDF, extracting pages...")
                        with fitz.open(temp_path) as pdf_doc:
                            pdf_name = (
                                metadata.lecture_title.replace(" ", "_")
                                if metadata.lecture_title
                                else os.path.splitext(os.path.basename(temp_path))[0]
                            )
                            for page_number in range(pdf_doc.page_count):
                                page: Page = pdf_doc.load_page(page_number)
                                page_img = f"{pdf_name}_page_{page_number + 1}.png"
                                pdf_page_path = os.path.join(tmpdir, page_img)
                                pix = page.get_pixmap()
                                pix.save(pdf_page_path)
                                temp_filepaths.append(pdf_page_path)
                                print(f"[INFO] Saved page {page_number + 1} as image: {pdf_page_path}")
                    case _:
                        print("[ERROR] Unsupported file type.")
                        return "Error"

            print(f"[INFO] Image paths for processing: {temp_filepaths}")
            graph_input = LectureInputState(
                image_paths=temp_filepaths,
                seperate_image=seperate_image,
                lecture_metadata=metadata,
            )
            print("[INFO] Invoking lecture processor graph...")
            result: LectureOutputState = await lecture_processor.ainvoke(graph_input)
            serialized_content = to_serializable(result)
            result = LectureOutputState.model_validate(serialized_content)
            print(f"[INFO] Lecture processor result: {result}")

            print("[INFO] Adding lecture package to database...")
            package = Package(name=metadata.lecture_title)
            session.add(package)
            session.commit()
            session.refresh(package)
            print_db_status(package, "Package")

            question_packages = result.gestalt_modules
            print(f"[INFO] Question packages to add: {question_packages}")
            if question_packages:
                created_folders = service.create_question_pack_v2(
                    package=package, qpacks=question_packages, session=session
                )
                print(f"[INFO] Created folders: {created_folders}")

            print("[INFO] Adding lecture summary file to database...")
            lecture_file = IndividualFile(
                filename="lecture_summary.md",
                content=result.generated_lecture.final_lecture,
                package_id=package.id,
            )
            service.create_file(lecture_file, session=session)
            session.commit()
            print_db_status(lecture_file, "Lecture Summary File")

        print("[INFO] Lecture processing complete. Returning result.")
        return result

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
