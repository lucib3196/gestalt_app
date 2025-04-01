from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel

from ..model.module_db import Module, Folder, File
from ..data import module as service
from ..data.module import get_session

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
def create_module(module: Module, session: Session = Depends(get_session)):
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

@router.get("/", response_model=List[Module])
def get_modules(session: Session = Depends(get_session)):
    return service.get_modules(session=session)


@router.get("/{module_id}", response_model=Module)
def get_module_by_id(module_id: int, session: Session = Depends(get_session)):
    return service.get_module_id(module_id, session)
