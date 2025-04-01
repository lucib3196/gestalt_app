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
    classes: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    reviewed: bool = False

class ModuleSimple(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    folders: List["Folder"] = Relationship(back_populates="module")

class Folder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    module_id: Optional[int] = Field(default=None, foreign_key="modulesimple.id")
    module: Optional[ModuleSimple] = Relationship(back_populates="folders")
    files: List["File"] = Relationship(back_populates="folder")

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    content: str
    folder_id: Optional[int] = Field(default=None, foreign_key="folder.id")
    folder: Optional[Folder] = Relationship(back_populates="files")