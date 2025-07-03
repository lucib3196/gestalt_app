from pydantic import BaseModel
from typing import Literal, Optional, Union, Any, Dict


class QuizData(BaseModel):
    params: Dict[str, Any]
    correct_answers: Dict[str, Any]
    intermediate: Optional[Dict[str, Any]] = None
    nDigits: int = 3
    sigfigs: int = 3


class QuizResponse(BaseModel):
    question_html: str
    solution_html: Optional[str]
    quiz_data: QuizData

class RenderedQuestion(BaseModel):
    question_html: str
    solution_html: str
    quiz_data: Optional[QuizData] = None
    
    
class CodeRunResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    quiz_response: Optional[QuizData] = None
    http_status_code: Optional[int] = None
