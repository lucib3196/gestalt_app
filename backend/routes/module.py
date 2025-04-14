from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from fastapi.responses import FileResponse, StreamingResponse
from ..data import crud as service
from ..data.database import get_session
from ..model.module_db import Module, Folder, File, ModuleSimple

# ────────────────────────────────────────────────
# 🚦 Router Configuration
# ────────────────────────────────────────────────

router = APIRouter(prefix="/modules")

# ────────────────────────────────────────────────
# 📦 Request Models
# ────────────────────────────────────────────────

class FolderCreateRequest(BaseModel):
    folder: Folder
    files_content: Dict[str, str]

# ────────────────────────────────────────────────
# 📤 POST Endpoints
# ────────────────────────────────────────────────

@router.post("/", response_model=Module)
def create_module(
    module: Module,
    session: Session = Depends(get_session)
):
    return service.create_module(module, session)


@router.post("/add_folder", response_model=Folder)
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

# Currently these are the main routes taht I should be working on 
@router.get("/simple/{module_id}/get_all_folders", response_model=List[Folder])
def get_all_folders(
    module_id:int,
    session:Session = Depends(get_session)):
    return service.get_module_folders(module_id=module_id,session=session)

@router.get("/simple/{module_id}/{folder_id}/get_all_files", response_model = List[File])
def get_folder_content(
        module_id:int,
        folder_id:int,
        session:Session = Depends(get_session)
    ):
        return service.get_folder_files(module_id,folder_id,session=session)

@router.get("/simple/{module_id}/{folder_id}/download", response_class=StreamingResponse)
def download_single_folder(
    module_id:int,
    folder_id:int,
    session: Session = Depends(get_session)
):
    return service.download_single_folder(module_id, folder_id, session)


@router.get("/simple/{module_id}/download", response_class=StreamingResponse)
def download_single_folder(
    module_id:int,
    session: Session = Depends(get_session)
):
    return service.download_all_folders_in_module(module_id, session)


# These still work but will need to refactor 
@router.get("/simple", response_model=List[ModuleSimple])
def get_modules(
    session: Session = Depends(get_session)
):
    return service.get_modules_simple(session=session)


@router.get("/simple/{module_id}", response_model=ModuleSimple)
def get_module_by_id(
    module_id: int,
    session: Session = Depends(get_session)
):
    return service.get_module_id(module_id, session)


@router.get("/simple/{module_id}/folder", response_model=Folder)
def get_module_folder(
    module_id: int,
    session: Session = Depends(get_session)
):
    return service.get_module_folder(module_id, session)


@router.get("/simple/{module_id}/folder/file_contents", response_model=List[File])
def get_modules_files(
    module_id: int,
    session: Session = Depends(get_session)
):
    return service.get_module_files(module_id, session)


@router.get("/simple/{module_id}/folder/file_contents/{file_id}")
def get_single_file(
    module_id: int,
    file_id: int,
    session: Session = Depends(get_session)
):
    return service.get_single_file(module_id, file_id, session)
