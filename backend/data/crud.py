# Contains CRUD service functions for your models.
from typing import List, Tuple, Dict, Any, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from .database import engine
from ..model.module_db import Module, Folder, File, ModuleSimple
import json



# Current Working Version With Simple Module

def get_module_folders(module_id:int, session: Session=None)->List[Folder]:
    # Basic check to ensure thet the module exist
    module = session.get(ModuleSimple, module_id)
    if not module: 
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Continuue and get the folder
    folders = session.query(Folder).filter_by(module_id=module_id).all()
    if not folders:
        raise HTTPException(status_code=404, detail="Folders not found")
    return folders
    
    
def get_folder_files(module_id:int,folder_id:int,session:Session=None)->List[File]:
    folders = get_module_folders(module_id=module_id,session=session)
    folder = session.query(Folder).filter_by(id=folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder.files
    
    
    

# These are a bit older and still work however i need to eventually move them and improve them 

def get_module_id(module_id: int, session: Session = None) -> ModuleSimple:
    module = session.get(ModuleSimple, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

def get_module_folder(module_id: int, session: Session = None) -> Folder:
    folder = session.query(Folder).filter_by(module_id=module_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

def get_module_files(module_id: int, session: Session) -> List[File]:
    folder = session.query(Folder).filter_by(module_id=module_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder.files  # Assumes relationship Folder.files is defined.

def get_modules_simple(skip: int = 0, limit: int = 10, session: Session = None) -> List[ModuleSimple]:
    return session.exec(select(ModuleSimple).offset(skip).limit(limit)).all()

def get_single_file(module_id: int, file_id: int, session: Session) -> str:
    file = (
        session.query(File)
        .join(Folder, File.folder_id == Folder.id)
        .filter(File.id == file_id, Folder.module_id == module_id)
        .first()
    )
    if not file:
        raise HTTPException(status_code=404, detail="File not found in this module")
    return file.content

def create_file(file: File, session: Session) -> File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def create_folder(folder: Folder, data: Dict[str, Any], session: Session) -> Folder:
    session.add(folder)
    session.commit()
    session.refresh(folder)
    if not isinstance(data, dict):
        data = data.dict()
    for filename, contents in data.items():
        if isinstance(contents, dict):
            contents = json.dumps(contents)
            
        file = File(name=filename, content=contents, folder_id=folder.id)
        create_file(file, session)
    return folder

def create_module_with_folders(
    module: ModuleSimple,
    folders: List[Tuple[str, Dict[str, Any]]],
    session: Session
) -> Module:
    session.add(module)
    session.commit()
    session.refresh(module)
    for title, files_content in folders:
        folder = Folder(name=title, module_id=module.id)
        create_folder(folder, files_content, session)
    return module


# Not Currently Active These are not yet implemented
def create_module(module: Module, session: Session) -> Module:
    session.add(module)
    session.commit()
    session.refresh(module)
    return module

def get_modules(skip: int = 0, limit: int = 10, session: Session = None) -> List[Module]:
    return session.exec(select(Module).offset(skip).limit(limit)).all()