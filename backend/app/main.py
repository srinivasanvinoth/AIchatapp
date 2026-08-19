from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, conversations, pdf_qa


tags_metadata = [
    {
        "name": "Authentication",
        "description": "User signup and login APIs."
    },
    {
        "name": "Users",
        "description": "Authenticated user profile APIs."
    },
    {
        "name": "Conversations",
        "description": "Create, read, update, delete conversations and messages."
    },
    {
        "name": "LangGraph PDF",
        "description": "Upload PDFs and answer questions using a LangGraph RAG workflow."
    }
]


app = FastAPI(
    title="React Chat API",
    description=(
        "FastAPI backend for the React + DynamoDB chat application. "
        "Use the Authentication APIs to sign up/login, copy the returned JWT, "
        "then click Authorize in Swagger and enter: Bearer <token>."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(pdf_qa.router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "running",
        "application": "Chat API",
        "swagger": "/swagger",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }
