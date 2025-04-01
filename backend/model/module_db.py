from typing import Optional, List
from sqlmodel import Field, SQLModel
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.types import JSON
from typing import Optional, List, ForwardRef
from sqlmodel import Field, Relationship, SQLModel


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    
class Module(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    topic: str
    difficulty: Difficulty
    classes: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    reviewed: bool = False

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    content: str
    folder_id: Optional[int] = Field(default=None, foreign_key="folder.id")
    folder: Optional["Folder"] = Relationship(back_populates="files")  # added back-reference


class Folder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    files: List[File] = Relationship(back_populates="folder")