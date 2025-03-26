from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session

from ..ai_workspace.agents.engineering_codegen.chains import graph as graph
from ..ai_workspace.agents.engineering_codegen.chains import OverallState

router = APIRouter(prefix="/chains")

@router.post('/', response_model=OverallState)
def run_chain(query:str):
    return graph.invoke({"query":query})