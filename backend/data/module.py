import os
from typing import Generator, Dict, Any,List, Tuple

from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import HTTPException
from pydantic import BaseModel
from ..model.module_db import Module, Folder, File, ModuleSimple
import json
# ────────────────────────────────────────────────
# 📦 Database Setup
# ────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

# Create all tables at startup
SQLModel.metadata.create_all(engine)

# ────────────────────────────────────────────────
# 🔌 Dependency Injection
# ────────────────────────────────────────────────

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# ────────────────────────────────────────────────
# 🛠️ CRUD Service Functions
# ────────────────────────────────────────────────

# ── Module ──────────────────────

def create_module(module: Module, session: Session) -> Module:
    session.add(module)
    session.commit()
    session.refresh(module)
    return module

def get_modules(skip: int = 0, limit: int = 10, session: Session = None):
    return session.exec(select(Module).offset(skip).limit(limit)).all()

def get_module_id(module_id: int, session: Session = None) -> ModuleSimple:
    module = session.get(ModuleSimple, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

def get_modules_simple(skip: int = 0, limit: int = 10, session: Session = None):
    return session.exec(select(ModuleSimple).offset(skip).limit(limit)).all()


# ── Folder & Files ─────────────

def create_file(file: File, session: Session) -> File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def create_folder(folder: Folder, data: Dict[str, Any], session: Session) -> Folder:
    session.add(folder)
    session.commit()
    session.refresh(folder)

    if not isinstance(data,dict):
        data = data.dict()
            
    for filename, contents in data.items():
        file = File(name=filename, content=contents, folder_id=folder.id)
        create_file(file, session)

    return folder

def create_module(module: ModuleSimple, folders: List[Tuple[str, Dict[str, Any]]], session: Session) -> Module:
    session.add(module)
    session.commit()
    session.refresh(module)

    for title, files_content in folders:
        folder = Folder(name=title, module_id=module.id)
        create_folder(folder, files_content, session)

    return module

    

        
        
        

