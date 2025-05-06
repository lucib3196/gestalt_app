"""
Routes for Package, Folder, and File operations.
"""

# ─────────────────────────────────────────────────────────────
# Standard Library Imports
# ─────────────────────────────────────────────────────────────
from typing import List, Dict, Any

# ─────────────────────────────────────────────────────────────
# Third-Party Imports
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlmodel import Session
from fastapi import FastAPI, Request, HTTPException
from typing import Union

# ─────────────────────────────────────────────────────────────
# Internal App Imports
# ─────────────────────────────────────────────────────────────
from ..data import question_models as service
from ..data.database import get_session
from ..model.question_models import Package, QuestionFolder, QuestionFile

# ─────────────────────────────────────────────────────────────
# Router Configuration
# ─────────────────────────────────────────────────────────────
router = APIRouter(prefix="/packages")


# ─────────────────────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────────────────────
class FolderCreateRequest(BaseModel):
    """
    Request model for creating a new folder with associated files.
    """

    folder: QuestionFolder
    files_content: Dict[str, str]


# ─────────────────────────────────────────────────────────────
# POST Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/", response_model=Package)
def create_package_route(
    package: Package, session: Session = Depends(get_session)
) -> Package:
    """
    Create a new package.
    """
    return service.create_package(package, session)


@router.post("/add_folder", response_model=QuestionFolder)
def create_folder_route(
    data: FolderCreateRequest, session: Session = Depends(get_session)
) -> QuestionFolder:
    """
    Create a new folder within a package along with its associated files.
    """
    return service.create_folder(
        folder=data.folder, data=data.files_content, session=session
    )


# ─────────────────────────────────────────────────────────────
# GET Endpoints
# ─────────────────────────────────────────────────────────────

# Retrieving all contents
@router.get("/get_all", response_model=List[Package])
def get_all_packages_route(session: Session = Depends(get_session)) -> List[Package]:
    """
    Retrieve all packages.
    """
    return service.get_packages(session=session)

@router.get(
    "/simple/{skip}/{limit}/get_all_folders", response_model=List[QuestionFolder]
)
def get_paginated_folders_route(
    skip: Union[str, int],
    limit: Union[str, int],
    session: Session = Depends(get_session),
) -> List[QuestionFolder]:
    """
    Retrieve a paginated list of question folders.
    """
    return service.get_all_question_folders(skip, limit, session)


@router.get("/question/{question_id}", response_model=QuestionFolder)
def get_question(question_id: int, session=Depends(get_session)) -> QuestionFolder:
    """Get a question from database

    Args:
        question_id (int): question id used to identify the question

    Returns:
        _type_: Question Folder object
    """
    return service.get_question_folder(question_id, session)


@router.get("/{package_id}/get_all_folders", response_model=List[QuestionFolder])
def get_all_folders_route(
    package_id: int, session: Session = Depends(get_session)
) -> List[QuestionFolder]:
    """
    Retrieve all question folders for the specified package.
    """
    return service.get_package_folders(package_id=package_id, session=session)

@router.get("/{question_id}/get_question_files")
def get_question_files_route(
    question_id:int,session:Session=Depends(get_session)
)->List[QuestionFile]:
    return service.get_all_question_files(folder_id=question_id,session=session)


@router.get(
    "/simple/{package_id}/{folder_id}/get_all_files", response_model=List[QuestionFile]
)
def get_files_for_folder_route(
    package_id: int, folder_id: int, session: Session = Depends(get_session)
) -> List[QuestionFile]:
    """
    Retrieve all question files for a specific folder within a package.
    """
    return service.get_folder_files(package_id, folder_id, session=session)


@router.get("/simple/{package_id}/{folder_id}/{filename}", response_model=QuestionFile)
def get_file_by_name(
    package_id: int,
    folder_id: int,
    filename: str,
    session: Session = Depends(get_session),
) -> QuestionFile:
    """
    Retrieve the content of a specific question file within a package.

    Args:
        package_id (int): The ID of the package.
        file_id (int): The ID of the file.
        session (Session): A SQLModel session.

    Returns:
        str: The file content.

    Raises:
        HTTPException: If the file is not found.
    """
    return service.get_single_file_name(package_id, folder_id, filename, session)


@router.get(
    "/simple/{package_id}/{folder_id}/download", response_class=StreamingResponse
)
def download_folder_route(
    package_id: int, folder_id: int, session: Session = Depends(get_session)
) -> StreamingResponse:
    """
    Download a specific question folder as a ZIP file.
    """
    return service.download_single_folder(
        package_id=package_id, folder_id=folder_id, session=session
    )


@router.get("/simple/{module_id}/download", response_class=StreamingResponse)
def download_all_folders_route(
    module_id: int, session: Session = Depends(get_session)
) -> StreamingResponse:
    """
    Download all folders for the specified package (module) as a master ZIP file.
    """
    return service.download_all_folders_in_module(module_id, session)


@router.get("/simple/{package_id}", response_model=Package)
def get_package_by_id_route(
    package_id: int, session: Session = Depends(get_session)
) -> Package:
    """
    Retrieve a package by its ID.
    """
    return service.get_package_by_id(package_id, session)


@router.get("/simple/{package_id}/folder", response_model=QuestionFolder)
def get_first_folder_route(
    package_id: int, session: Session = Depends(get_session)
) -> QuestionFolder:
    """
    Retrieve the first question folder associated with the specified package.
    """
    return service.get_package_folder(package_id, session)


@router.get(
    "/simple/{package_id}/folder/file_contents", response_model=List[QuestionFile]
)
def get_files_from_folder_route(
    package_id: int, session: Session = Depends(get_session)
) -> List[QuestionFile]:
    """
    Retrieve all question files from the first folder of the specified package.
    """
    return service.get_package_files(package_id, session)


@router.get("/simple/{package_id}/folder/file_contents/{file_id}")
def get_file_content_route(
    package_id: int, file_id: int, session: Session = Depends(get_session)
):
    """
    Retrieve the content of a specific question file within a package.
    """
    return service.get_single_file(package_id, file_id, session)


@router.get("simple/{question_folder_id}")
def get_question_folder_id(
    question_folder_id: int, session: Session = Depends(get_session)
):
    return service.get_question_folder(question_folder_id, session)


@router.get("/simple/{question_folder_id}/files")
def get_question_folder_id(
    question_folder_id: int, session: Session = Depends(get_session)
):
    return service.get_all_question_files(question_folder_id, session)


class FileUpdate(BaseModel):
    question_folder_id: int
    question_file_name: str
    content: str


@router.post("/simple/update_code")
async def update_filecontents(
    update: FileUpdate,
    session: Session = Depends(get_session),
) -> dict:
    try:
        service.update_filecontents(
            folder_id=update.question_folder_id,
            file_name=update.question_file_name,
            new_content=update.content,
            session=session,
        )
    except Exception as e:
        print(f"Error updating file contents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Success"}
