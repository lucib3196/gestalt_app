from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum



class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    
class Module(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True)
    title: str
    topic: str
    difficulty: Difficulty
    reviewed:bool = False
    
