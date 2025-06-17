from ..data import generate_quiz as quiz_service
from ..data.generate_quiz import QuizData, GenerateQuizResponse, CodeRunResponse
from fastapi import APIRouter, HTTPException, Query
from ..data.database import get_session
from sqlmodel import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, status
from fastapi import Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/quiz")
from typing import Dict, Any, Literal
import ast


class QuizArg(BaseModel):
    server_type: Literal["javascript", "python"]


@router.post(
    "/adaptive_quiz/get_quiz/{question_folder_id}", response_class=HTMLResponse
)
async def get_adaptive_quiz(
    request: Request,
    question_folder_id: int,
    data: QuizArg,
    session: Session = Depends(get_session),
):
    response: CodeRunResponse = await quiz_service.generate_quiz(
        question_folder_id, server_type=data.server_type, session=session
    )
    if response.success and isinstance(response.result, GenerateQuizResponse):
        quiz_data = response.result.quiz_data
        
        if isinstance(quiz_data, BaseModel):
            request.session["quiz_data"] = quiz_data.model_dump()
        else:
            request.session["quiz_data"] = quiz_data
        
        request.session["solution_html"] = response.result.solution_html
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"html": response.result.question_html},
        )
    else:
        # Return JSON with an explicit “detail” field and proper HTTP status
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": response.error},
        )


@router.post(
    "/adaptive_quiz/get_solution/{question_folder_id}", response_class=HTMLResponse
)
async def get_solution_html(
    request: Request,
    question_folder_id: int,
    data: QuizArg,
    session: Session = Depends(get_session),
):
    # Try to get pre-generated content from session
    cached_quiz_data = request.session.get("quiz_data")
    cached_solution = request.session.get("solution_html")
    cached_server_type = request.session.get("server_type")

    # When cachine ensure that the solution html is based on the most recent server type if it changes well deal with it
    if (
        cached_quiz_data
        and cached_solution
        and cached_server_type == data.server_type  # <-- ensure match
    ):
        return HTMLResponse(content=cached_solution)

    # Generate quiz if not in session
    response: CodeRunResponse = await quiz_service.generate_quiz(
        question_folder_id, server_type=data.server_type, session=session
    )

    if response.success:
        # Cache quiz and solution
        request.session["quiz_data"] = response.result.quiz_data.model_dump()
        request.session["solution_html"] = response.result.solution_html
        return HTMLResponse(content=response.result.solution_html)
    else:
        return HTMLResponse(content=response.error, status_code=405)


@router.post("/adaptive_quiz/grade_quiz")
async def submit_quiz(request: Request, data: Dict[str, Any]):
    quiz_data = request.session.get("quiz_data")
    if not quiz_data:
        raise HTTPException(status_code=400, detail="No quiz data found in session.")
    # Proceed with validation using quiz_data["params"] and quiz_data["correct_answers"]
    return quiz_data.get("correct_answers")
