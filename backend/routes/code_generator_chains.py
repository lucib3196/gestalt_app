from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from ..data.module import get_session
from ..data import crud as service
from ..model.module_db import ModuleSimple
from ..ai_workspace.agents.engineering_codegen.code_generator import (
    QuestionPayload,
    InitialMetadata,
    QuestionPackage,
    FilesData,
    QuestionMetadata,
    compiled_graph as graph,
)
from .utils import save_generated_module

# Version 1 router
router = APIRouter(prefix="/code_generator_chains/v1")


class QuestionData(BaseModel):
    """
    Input model for the V1 code generator.
    Accepts a question and the name for the folder/module to be created.
    """

    question: str
    folder_name: str


@router.post("/", response_model=QuestionPackage)
async def generate_question_module_v1(
    data: QuestionData, session: Session = Depends(get_session)
) -> QuestionPackage:
    """
    Version 1 endpoint for generating a question module using the code generation graph.

    This version only takes in a simple question string and produces metadata, files,
    and module structure which is stored in the database.
    """

    # Static metadata for initial generation
    initial_metadata: InitialMetadata = InitialMetadata(
        createdBy="lberm007@ucr.edu",
        qtype="num",
        nSteps=1,
        updatedBy="",
        codelang="JavaScript",
        reviewed="False",
        ai_generated="True",
    )

    # Input payload for the LLM pipeline
    question_payload: QuestionPayload = QuestionPayload(
        question=data.question,
        solution_guide=None,
        additional_instructions=None,
    )

    graph_input: QuestionPackage = QuestionPackage(
        question_payload=question_payload,
        initial_metadata=initial_metadata,
    )

    # Call the LLM graph
    response: QuestionPackage = await graph.ainvoke(graph_input)

    response = QuestionPackage(**response)

    # Extract output
    question_metadata: QuestionMetadata = response.question_metadata
    question_files: FilesData = response.files
    question_title: str = question_metadata.title

    module_content = [(question_title, question_files)]

    # Save to DB
    await save_generated_module(
        folders=module_content, title=data.folder_name, session=session
    )

    return response
