from pydantic import BaseModel, Field


class PDFQuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=10000
    )


class PDFQuestionResponse(BaseModel):
    answer: str
    sources: list[dict]
