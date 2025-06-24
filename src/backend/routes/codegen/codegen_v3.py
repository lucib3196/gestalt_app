# =========================
# Imports and Configuration
# =========================

# --- Standard Library Imports ---
import os
import tempfile
import shutil
import asyncio
from datetime import date, datetime

# --- Third-Party Imports ---
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlmodel import Session
from pydantic import BaseModel, ValidationError
from typing import List

# --- Local Application Imports ---
from ai_workspace.agentsv2.code_generator.ver3.code_generator import (
    compiled_graph as code_generator,
    CodeGenInput,
    CodeGenOutput,
)
from backend.data.module import (
    QuestionFolder,
    Package,
    File as IndividualFile,
    get_session,
)
from backend.data import question_models as service
from schemas import InitialMetadata, Question
from ai_workspace.agentsv2.image_codegenerator.agent import (
    compiled_graph as image_codegenator,
    StateInput as ImageInputState,
    StateOutput,
)

# --- FastAPI Router Setup ---
router = APIRouter(prefix="/codegen_v3")

# --- Allowed MIME Types ---
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "application/pdf"}

# --- Input Schema ---
class QuestionData(BaseModel):
    """
    Input model for the V2 text-based generator.
    Accepts a question and the name of the module to be created.
    """
    questions: List[str]
    package_name: str

# --- Initial Metadata (Dynamic per user, example shown) ---
initial_metadata = InitialMetadata(
    createdBy="lberm007@ucr.edu",
    qtype="num",
    nSteps=1,
    updatedBy="",
    codelang="JavaScript",
    reviewed="False",
    ai_generated="True",
)

def create_question_pack_v3(
    package: Package, qpacks: List[CodeGenOutput], session: Session
) -> List[QuestionFolder]:
    created_folders: List[QuestionFolder] = []

    for raw_pack in qpacks:
        try:
            qpack = (
                CodeGenOutput(**raw_pack)
                if not isinstance(raw_pack, CodeGenOutput)
                else raw_pack
            )

            q_metadata = qpack.q_metadata
            q_initial_metadata = qpack.initial
            q_files = qpack.files

            ai_gen_flag = bool(q_initial_metadata.ai_generated) if q_initial_metadata else True
            creator = q_initial_metadata.createdBy if q_initial_metadata else ""

            question_folder = QuestionFolder(
                title=q_metadata.title,
                topic=q_metadata.topic,
                tags=q_metadata.tags,
                pre_reqs=q_metadata.prereqs,
                is_adaptive=ai_gen_flag,
                relevant_courses=q_metadata.relevant_courses,
                reviewers=[],
                reviewed=False,
                created_by=creator,
                package_id=package.id,
            )

            data = {
                "question.html": q_files.question_html,
                "solution.html": q_files.solution_html,
                "server.js": q_files.server_js,
                "server.py": q_files.server_py,
                "info.json": q_files.metadata,
            }

            saved_folder = service.create_question_folder(
                question_folder, data=data, session=session
            )
            created_folders.append(saved_folder)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating question folder: {e}")

    return created_folders


@router.post("/text", response_model=List[CodeGenOutput])
async def gen_question_text_v3(
    data: QuestionData, session: Session = Depends(get_session)
):
    try:
        tasks = [
            code_generator.ainvoke(
                CodeGenInput(
                    question_payload=Question(question=q),  # type: ignore
                    initial_metadata=initial_metadata,
                )
            )
            for q in data.questions
        ]

        question_packages_raw = await asyncio.gather(*tasks)
        question_packages: List[CodeGenOutput] = [
            CodeGenOutput(**pkg) if not isinstance(pkg, CodeGenOutput) else pkg
            for pkg in question_packages_raw
        ]

        package = Package(name=data.package_name)
        session.add(package)
        session.commit()
        session.refresh(package)

        create_question_pack_v3(package=package, qpacks=question_packages, session=session)

        return question_packages

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-based question generation failed: {e}")


@router.post("/image", response_model=List[CodeGenOutput])
async def generate_question_image_v3(
    files: List[UploadFile] = File(...),
    package_name: str = Form(...),
    session: Session = Depends(get_session),
):
    try:
        temp_filepaths = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for file in files:
                temp_path = os.path.join(tmpdir, file.filename)  # type: ignore
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                temp_filepaths.append(temp_path)

            graph_input = ImageInputState(
                image_paths=temp_filepaths, initial_metadata=initial_metadata  # type: ignore
            )

            raw_result = await image_codegenator.ainvoke(graph_input)
            output = raw_result.get("output",{})
            question_packages: List[CodeGenOutput] = []
            print("This is the output", output)
            for pkg in output:
                if hasattr(pkg, "dict"):
                    question_packages.append(CodeGenOutput(**pkg.dict()))
                elif isinstance(pkg, dict):
                    question_packages.append(CodeGenOutput(**pkg))
                else:
                    raise TypeError(f"Expected dict or object with .dict(), got {type(pkg)}")

            package = Package(name=package_name)
            session.add(package)
            session.commit()
            session.refresh(package)

            create_question_pack_v3(
                package=package, qpacks=question_packages, session=session
            )

            return question_packages

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image-based question generation failed: {e}")