from fastapi import APIRouter
from ..model.module import Module
from ..fake import module as service
from typing import List

router = APIRouter(prefix = '/modules')

@router.get("/", response_model=List[Module])
def get_all()->list[Module]:
    return service.get_all()

# @router.get("/{id}", response_model=Module)
# def get_by_id(id:int)->Module:
#     for module in fake_modules:
#         if module.id == id:
#             return module
#     return None