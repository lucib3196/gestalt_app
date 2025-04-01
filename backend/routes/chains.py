from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel

from ..model.module_db import Module, Folder, File
from ..data import module as service
from ..ai_workspace.agents.engineering_codegen.chains import graph, OverallState
from ..data.module import get_session

router = APIRouter(prefix="/chains")

class QueryRequest(BaseModel):
    query: str
    folder_name: str


@router.post("/", response_model=OverallState)
def run_chain(data: QueryRequest, session: Session = Depends(get_session)):
    # Step 1: Run AI chain
    result = graph.invoke({"query": data.query})

    # Step 2: Extract folder name and file data
    folder_name = data.folder_name
    files_content = result  # Make sure this is a dict[str, str]

    # Step 3: Create folder and files
    folder = Folder(name=folder_name)
    created_folder = service.create_folder(folder, data=files_content, session=session)
    return result
