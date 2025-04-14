from fastapi import APIRouter, Depends, UploadFile, File, Form
from pydantic import BaseModel
from sqlmodel import Session
from typing import List, Tuple
import os
import shutil
import tempfile
from ast import literal_eval


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


router = APIRouter(prefix="/code_generator_chains/v1")


class QuestionData(BaseModel):
    """
    Input model for the V1 text-based generator.
    Accepts a question and the name of the module to be created.
    """

    questions: List[str]
    package_name: str

def create_package_with_folders(package_title:str,question_packages:List[QuestionPackage],session: Session):
    package = Package(title=package_title)
    session.add(package)
    session.commit()
    session.refresh(package)
    
    
    for q_pack in question_packages:
        if not isinstance(q_pack,QuestionPackage):
            q_pack = QuestionPackage(**q_pack)
            
        q_metadata:QuestionMetadata = q_pack.question_metadata
        q_files = q_pack.files
        initial_metadata:TextInitialMetadata = q_pack.initial_metadata
        
        folder = QuestionFolder(
            title=q_metadata.title,
            topic = q_metadata.topic,
            tags=q_metadata.tags,
            pre_reqs=q_metadata.prereqs,
            is_adaptive=literal_eval(q_metadata.isAdaptive),
            ai_generated=literal_eval(initial_metadata.ai_generated),
            reviewers=None,
            reviewed=False,
            created_by=initial_metadata.createdBy,
            package_id=package.id
        )
        service.create_folder(folder,data=q_files,session=session)
    return package


@router.post("/", response_model=List[QuestionPackage])
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
            question = question,
            solution_guide=None,
            additional_instructions=None
        )
        graph_input = QuestionPackage(
            question_payload=question_payload,
            initial_metadata=initial_metadata
        )
        tasks.append(graph.ainvoke(graph_input))
    
    question_packages:List[QuestionPackage] =  await asyncio.gather(*tasks)
    create_package_with_folders(package_title=data.package_name, question_packages=question_packages,session=session)
    return question_packages



        
    

@router.post("/image_upload", response_model=ImageExtractionOutputState)
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
        create_package_with_folders(package_title=folder_name, question_packages=q_packages,session=session)
    return response
