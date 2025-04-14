from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from fastapi.responses import FileResponse, StreamingResponse
from ..data import question_models as service
from ..data.database import get_session
from ..model.question_models import Package, QuestionFolder, QuestionFile

# ────────────────────────────────────────────────
# 🚦 Router Configuration
# ────────────────────────────────────────────────

router = APIRouter(prefix="/packages")

# ────────────────────────────────────────────────
# 📦 Request Models
# ────────────────────────────────────────────────

class FolderCreateRequest(BaseModel):
    folder: QuestionFolder
    files_content: Dict[str, str]

# ────────────────────────────────────────────────
# 📤 POST Endpoints
# ────────────────────────────────────────────────

@router.post("/", response_model=Package)
def create_package(
    package: Package,
    session: Session = Depends(get_session)
):
    return service.create_package(package, session)


@router.post("/add_folder", response_model=QuestionFolder)
def create_folder(
    data: FolderCreateRequest,
    session: Session = Depends(get_session)
):
    return service.create_folder(
        folder=data.folder,
        data=data.files_content,
        session=session
    )

# ────────────────────────────────────────────────
# 📥 GET Endpoints
# ────────────────────────────────────────────────

@router.get("/simple/{package_id}/get_all_folders", response_model=List[QuestionFolder])
def get_all_folders(
    package_id: int,
    session: Session = Depends(get_session)
):
    return service.get_package_folders(package_id=package_id, session=session)


@router.get("/simple/{package_id}/{folder_id}/get_all_files", response_model=List[QuestionFile])
def get_folder_content(
    package_id: int,
    folder_id: int,
    session: Session = Depends(get_session)
):
    return service.get_folder_files(package_id, folder_id, session=session)

@router.get("/simple/{package_id}/{folder_id}/download", response_class=StreamingResponse)
def download_single_folder(
    package_id:int,
    folder_id:int,
    session: Session = Depends(get_session)
):
    return service.download_single_folder(package_id=package_id, folder_id=folder_id, session=session)


@router.get("/simple/{module_id}/download", response_class=StreamingResponse)
def download_single_folder(
    module_id:int,
    session: Session = Depends(get_session)
):
    return service.download_all_folders_in_module(module_id, session)

@router.get("/simple", response_model=List[Package])
def get_packages(
    session: Session = Depends(get_session)
):
    return service.get_packages(session=session)


@router.get("/simple/{package_id}", response_model=Package)
def get_package_by_id(
    package_id: int,
    session: Session = Depends(get_session)
):
    return service.get_package_by_id(package_id, session)


@router.get("/simple/{package_id}/folder", response_model=QuestionFolder)
def get_package_folder(
    package_id: int,
    session: Session = Depends(get_session)
):
    return service.get_package_folder(package_id, session)


@router.get("/simple/{package_id}/folder/file_contents", response_model=List[QuestionFile])
def get_package_files(
    package_id: int,
    session: Session = Depends(get_session)
):
    return service.get_package_files(package_id, session)


@router.get("/simple/{package_id}/folder/file_contents/{file_id}")
def get_single_file(
    package_id: int,
    file_id: int,
    session: Session = Depends(get_session)
):
    return service.get_single_file(package_id, file_id, session)
