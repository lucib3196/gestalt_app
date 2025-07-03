from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlmodel import Session
from typing import Any, Dict, Literal, Union, Optional
from ..data import generate_quiz as quiz_service
from ..data.generate_quiz import CodeRunResponse, QuizData
from ..data.database import get_session
from question_rendering import RenderedQuestion
from ai_workspace.utils import to_serializable

router = APIRouter(prefix="/quiz")


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
) -> JSONResponse:
    """
    Generate a fresh adaptive quiz and store relevant data in the session.
    Returns the rendered quiz HTML or an error message.
    """
    quiz_response: Union[CodeRunResponse, RenderedQuestion] = (
        await quiz_service.generate_quiz(
            question_folder_id, server_type=data.server_type, session=session
        )
    )

    if isinstance(quiz_response, CodeRunResponse):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": quiz_response.error},
        )

    if isinstance(quiz_response, RenderedQuestion) and quiz_response.quiz_data:
        # Ensure session is available and mutable
        if not hasattr(request, "session"):
            raise HTTPException(status_code=500, detail="Session middleware not configured.")
        # Store quiz data as a dict to avoid serialization issues
        request.session["quiz_data"] = quiz_response.quiz_data.model_dump()
        request.session["server_type"] = data.server_type
        request.session["solution_html"] = quiz_response.solution_html
        request.session["question_id"] = question_folder_id

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"html": quiz_response.question_html},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Failed to generate quiz."},
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
    cached_solution_html = request.session.get("solution_html")
    cached_server_type: Optional[Literal["javascript", "python"]] = request.session.get(
        "server_type"
    )
    if (
        cached_solution_html
        and request.session.get("question_id") == question_folder_id
    ):
        return HTMLResponse(content=cached_solution_html)

    if cached_server_type is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "No server_type found in session."},
        )

    quiz_response: Union[CodeRunResponse, RenderedQuestion] = (
        await quiz_service.generate_quiz(
            question_folder_id, server_type=cached_server_type, session=session
        )
    )
    if isinstance(quiz_response, CodeRunResponse):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": getattr(quiz_response, "error", "Unknown error")},
        )
    if isinstance(quiz_response, RenderedQuestion) and quiz_response.quiz_data:
        # Update session with latest quiz data and solution
        request.session["quiz_data"] = quiz_response.quiz_data.model_dump()
        request.session["solution_html"] = quiz_response.solution_html
        request.session["question_id"] = question_folder_id
        return HTMLResponse(content=quiz_response.solution_html)


@router.post("/adaptive_quiz/grade_quiz")
async def submit_quiz(
    request: Request,
    session: Session = Depends(get_session),
):
    quiz_data = request.session.get("quiz_data")
    if not quiz_data:
        raise HTTPException(status_code=400, detail="No quiz data found in session.")
    # Proceed with validation using quiz_data["params"] and quiz_data["correct_answers"]
    return quiz_data.get("correct_answers")
