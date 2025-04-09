from ..data import generate_quiz as quiz_service
from fastapi import APIRouter, HTTPException, Query
from ..data.database import get_session
from sqlmodel import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends

router =  APIRouter(prefix="/quiz")


@router.post("/adaptive_quiz/{module_id}", response_class=HTMLResponse)
async def get_adaptive_quiz(module_id:int, session: Session = Depends(get_session)):
    content = await quiz_service.generate_quiz(module_id, session)
    return HTMLResponse(content=content)