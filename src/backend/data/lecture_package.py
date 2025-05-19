from ..model.question_models import LecturePackage,IndividualFile
from .database import engine
from ..model.question_models import Package, QuestionFolder, QuestionFile
from sqlmodel import Session, select
from typing import Dict, Optional, List
import json

# Create Methods
def create_file(file:IndividualFile, session: Session):
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def create_codefile(file:QuestionFile,session:Session):
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def create_package(package: LecturePackage, session: Session):
    session.add(package)
    session.commit()
    session.refresh(package)
    return package

def create_gestalt_module(
    module:QuestionFolder, data:Dict[str,any], session=Session):
    
    # Add folder 
    session.add(module)
    session.commit()
    session.refresh()
    
    if not isinstance(data,dict):
        data = data.dict()
    for filename, contents in data.items():
        if isinstance(contents,dict):
            contents = json.dumps(contents)
        file = QuestionFile(
            name=filename,
            content=contents,
            save_name=filename,
            question_folder=module.id
        )
        create_codefile(file,session)
    return module

