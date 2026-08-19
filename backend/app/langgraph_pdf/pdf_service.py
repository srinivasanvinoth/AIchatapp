from pathlib import Path
import shutil
import uuid

from fastapi import HTTPException, UploadFile

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


BACKEND_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_ROOT = BACKEND_ROOT / "data" / "uploads"
VECTOR_ROOT = BACKEND_ROOT / "data" / "vectorstores"

UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
VECTOR_ROOT.mkdir(parents=True, exist_ok=True)


def _embeddings() -> GoogleGenerativeAIEmbeddings:
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured."
        )

    return GoogleGenerativeAIEmbeddings(
        model=settings.GEMINI_EMBEDDING_MODEL,
        google_api_key=settings.GEMINI_API_KEY
    )


def user_vector_path(user_id: str) -> Path:
    return VECTOR_ROOT / user_id


def upload_pdf_for_user(user_id: str, file: UploadFile) -> dict:
    filename = file.filename or "document.pdf"

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    user_upload_dir = UPLOAD_ROOT / user_id
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4()}-{Path(filename).name}"
    pdf_path = user_upload_dir / stored_name

    with pdf_path.open("wb") as output:
        shutil.copyfileobj(file.file, output)

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    if not documents:
        raise HTTPException(
            status_code=400,
            detail="The PDF did not contain readable text."
        )

    for doc in documents:
        doc.metadata["source_file"] = filename
        doc.metadata["owner_user_id"] = user_id

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No searchable chunks could be created from the PDF."
        )

    vector_path = user_vector_path(user_id)

    # Each new upload is added to the signed-in user's existing PDF knowledge base.
    if (vector_path / "index.faiss").exists():
        current = FAISS.load_local(
            str(vector_path),
            _embeddings(),
            allow_dangerous_deserialization=True
        )
        current.add_documents(chunks)
        vector_store = current
    else:
        vector_store = FAISS.from_documents(
            chunks,
            _embeddings()
        )

    vector_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(vector_path))

    return {
        "file_name": filename,
        "pages": len(documents),
        "chunks": len(chunks),
        "message": "PDF uploaded and indexed successfully."
    }


def load_user_vector_store(user_id: str) -> FAISS:
    vector_path = user_vector_path(user_id)

    if not (vector_path / "index.faiss").exists():
        raise HTTPException(
            status_code=404,
            detail="No PDF has been indexed for this user. Upload a PDF first."
        )

    return FAISS.load_local(
        str(vector_path),
        _embeddings(),
        allow_dangerous_deserialization=True
    )


def retrieve_pdf_context(user_id: str, question: str) -> list[dict]:
    vector_store = load_user_vector_store(user_id)

    documents = vector_store.similarity_search(
        question,
        k=settings.PDF_TOP_K
    )

    return [
        {
            "content": doc.page_content,
            "page": doc.metadata.get("page"),
            "source_file": doc.metadata.get("source_file")
        }
        for doc in documents
    ]
