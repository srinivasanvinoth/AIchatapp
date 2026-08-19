from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies.auth import get_current_user
from app.langgraph_pdf.graph import ask_pdf
from app.langgraph_pdf.pdf_service import upload_pdf_for_user
from app.models.pdf_qa import PDFQuestionRequest


router = APIRouter(
    prefix="/api/pdf",
    tags=["LangGraph PDF"]
)


@router.post("/upload")
def upload_pdf(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    return upload_pdf_for_user(
        current_user["user_id"],
        file
    )


@router.post("/ask")
def ask_pdf_question(
    request: PDFQuestionRequest,
    current_user=Depends(get_current_user)
):
    return ask_pdf(
        current_user["user_id"],
        request.question
    )
