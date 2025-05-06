from ..data import generate_quiz as quiz_service
from ..data.generate_quiz import QuizData, GenerateQuizResponse,CodeRunResponse
from fastapi import APIRouter, HTTPException, Query
from ..data.database import get_session
from sqlmodel import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends
from fastapi import Request
from pydantic import BaseModel
router = APIRouter(prefix="/quiz")
from typing import Dict, Any,Literal
import ast

class QuizArg(BaseModel):
    server_type : Literal['javascript','python']

@router.post("/adaptive_quiz/get_quiz/{question_folder_id}", response_class=HTMLResponse)
async def get_adaptive_quiz(
    request: Request, question_folder_id: int,data:QuizArg, session: Session = Depends(get_session)
):
    print(f"This is the server" ,data.server_type)
    response: CodeRunResponse = await quiz_service.generate_quiz(question_folder_id,server_type=data.server_type, session=session)
    if response.success:
        request.session["quiz_data"] = response.result.quiz_data.model_dump()
        return HTMLResponse(content=response.result.question_html)
    else:
        return HTMLResponse(content=response.error, status_code=405)


@router.post("/adaptive_quiz/grade_quiz")
async def submit_quiz(request: Request, data: Dict[str, Any]):
    quiz_data = request.session.get("quiz_data")
    if not quiz_data:
        raise HTTPException(status_code=400, detail="No quiz data found in session.")
    # Proceed with validation using quiz_data["params"] and quiz_data["correct_answers"]
    return quiz_data.get("correct_answers")
