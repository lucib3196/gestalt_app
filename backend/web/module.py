from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session

from ..model.module_db import Module
from ..data import module as service
from ..data.module import get_session

router = APIRouter(prefix="/modules")

@router.post("/", response_model=Module)
def create_module(module: Module, session: Session = Depends(get_session)):
    return service.create_module(module, session)

@router.get("/", response_model=List[Module])
def get_modules(session: Session = Depends(get_session)):
    return service.get_modules(session=session)

@router.get("/{module_id}", response_model=Module)
def get_module_by_id(module_id: int, session: Session = Depends(get_session)):
    return service.get_module_id(module_id, session)
