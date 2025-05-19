from pydantic import BaseModel
from typing import Literal, Optional, Union, Any, Dict


class QuizData(BaseModel):
    params: Dict[str, Union[str, int, float]]
    correct_answers: Dict[str, Union[str, int, float]]
    nDigits: Optional[int] = None
    sigfigs: Optional[int] = None


class GenerateQuizResponse(BaseModel):
    question_html: str
    quiz_data: Union[QuizData, dict]
    solution_html: Optional[str]


class ServerType(BaseModel):
    server_type: Literal["javascript", "python"]


class CodeRunResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    result: Optional[Union[GenerateQuizResponse, QuizData, dict]] = None
    http_status_code: Optional[int] = None
