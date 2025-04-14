from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.types import JSON

class Package(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    question_folders: List["QuestionFolder"] = Relationship(back_populates="package")


class QuestionFolder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Question Information 
    title: str
    topic: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    pre_reqs: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    is_adaptive: Optional[bool] = None
    ai_generated: Optional[bool] = True
    # Data for who is reviewing 
    created_by: Optional[str] = None
    reviewers: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    reviewed: Optional[bool] = False
    # Relationships
    package_id: Optional[int] = Field(default=None, foreign_key="package.id")
    package: Optional[Package] = Relationship(back_populates="question_folders")
    question_files: List["QuestionFile"] = Relationship(back_populates="question_folder")

class QuestionFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    content: str
    save_name: str
    question_folder_id: Optional[int] = Field(default=None, foreign_key="questionfolder.id")
    question_folder: Optional[QuestionFolder] = Relationship(back_populates="question_files")
