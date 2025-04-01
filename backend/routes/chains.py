from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel

from ..model.module_db import Module, Folder, File, ModuleSimple
from ..data import module as service
from ..ai_workspace.agents.engineering_codegen.chains import graph, OverallState, InitialMetadata, OutputState
from ..data.module import get_session

router = APIRouter(prefix="/chains")

class QueryRequest(BaseModel):
    query: str
    folder_name: str


@router.post("/", response_model=OutputState)
def run_chain(data: QueryRequest, session: Session = Depends(get_session)):
    
    # Step 0 Initialize Metadata (this shoudl be changed eventually)
    metadata_dict = {
        "createdBy": "lberm007@ucr.edu",
        "qtype": "num",
        "nSteps": 1,
        "updatedBy": "",
        "difficulty": 1,
        "codelang": "javascript",
        "reviewed": "False",
        "ai_generated": "True"
    }
    initial_metadata = InitialMetadata(**metadata_dict)
    # Step 1: Run AI chain
    result = graph.invoke({"query": data.query,"initial_metadata":initial_metadata })
    
    files_content = result.get("files_data")
    title = result.get("title")
    folders = [(title, files_content)]
    
    # Step 3: Create folder and files
    module = ModuleSimple(name=title)
    created_module = service.create_module(module, folders = folders, session=session)
    return result
