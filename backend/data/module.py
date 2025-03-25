import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import HTTPException
from ..model.module_db import Module

# Define path to save engine and create 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

# Create all tables
SQLModel.metadata.create_all(engine)

# Dependency: Get the session
def get_session():
    with Session(engine) as session:
        yield session



# Service functions 
def create_module(module: Module, session: Session):
    session.add(module)
    session.commit()
    session.refresh(module)
    return module

def get_modules(skip: int = 0, limit: int = 10, session: Session = None):
    modules = session.exec(select(Module).offset(skip).limit(limit)).all()
    return modules

def get_module_id(module_id: int, session: Session = None):
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module
