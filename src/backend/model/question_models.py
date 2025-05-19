from typing import List, Optional
from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel


class Package(SQLModel, table=True):
    __tablename__ = "package"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationships
    files: List["File"] = Relationship(back_populates="package")
    question_modules: List["QuestionFolder"] = Relationship(back_populates="package")


class QuestionFolder(SQLModel, table=True):
    __tablename__ = "question_folder"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    # JSON‐typed metadata with empty list defaults
    topic: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    pre_reqs: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    is_adaptive: Optional[bool] = Field(default=None)
    ai_generated: bool = Field(default=True)
    created_by: Optional[str] = Field(default=None)
    reviewers: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    reviewed: bool = Field(default=False)

    # Foreign key + relationship to Package
    package_id: Optional[int] = Field(default=None, foreign_key="package.id")
    package: Optional[Package] = Relationship(back_populates="question_modules")

    # Relationship to File
    files: List["File"] = Relationship(back_populates="question_folder")


class File(SQLModel, table=True):
    __tablename__ = "file"

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: str

    # Relationship to Package
    package_id: Optional[int] = Field(default=None, foreign_key="package.id")
    package: Optional[Package] = Relationship(back_populates="files")

    # Relationship to QuestionFolder
    question_folder_id: Optional[int] = Field(
        default=None, foreign_key="question_folder.id"
    )
    question_folder: Optional[QuestionFolder] = Relationship(back_populates="files")


class PackageContents(BaseModel):
    package: Package
    questions: List[QuestionFolder] = Field(default=[])
    files: List[File] = Field(default=[])
