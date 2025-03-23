from fastapi import APIRouter
from model.module import Module, Difficulty, SpecificClass
import fake.module as service
from typing import List

router = APIRouter(prefix = '/modules')

@router.get("/", response_model=List[Module])
def get_all()->list[Module]:
    return service.get_all()

@router.get("/{id}", response_model=Module)
def get_by_id(id:int)->Module:
    return service.get_by_id(id)