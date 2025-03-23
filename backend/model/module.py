from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class SpecificClass(BaseModel):
    id: Optional[int] = None
    class_name: str
    professor: Optional[str] = None
    class_description: str
    
class Module(BaseModel):
    id: Optional[int] = None
    title: str
    topic:str
    specific_class: Optional[List[SpecificClass]] = Field(default_factory=list)
    subtopic:Optional[str]
    question:str
    solution_summary:str
    difficulty: Difficulty
    tags: List[str] = Field(default_factory=list)
    has_diagram:bool = False
    created_by: Optional[str]=None
    reviewed:bool=False