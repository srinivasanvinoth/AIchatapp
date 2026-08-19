from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.langgraph_pdf.pdf_service import retrieve_pdf_context


PDF_QA_SYSTEM_PROMPT = """
You are a PDF question-answering assistant.

Your job is to answer the user's question using ONLY the PDF context supplied
to you.

Rules:
1. Use the retrieved PDF context as the source of truth.
2. Do not invent facts that are not present in the PDF context.
3. If the answer cannot be determined from the retrieved context, say:
   "I could not find enough information in the uploaded PDF to answer that."
4. Give a clear and concise answer.
5. When useful, mention the source PDF name and page number.
6. Do not claim to have read pages or files that are not included in the context.
7. If different retrieved passages conflict, explicitly mention the conflict.
""".strip()


class PDFQuestionState(TypedDict, total=False):
    user_id: str
    question: str
    context_items: list[dict]
    context_text: str
    answer: str


def retrieve_node(state: PDFQuestionState) -> PDFQuestionState:
    items = retrieve_pdf_context(
        state["user_id"],
        state["question"]
    )

    sections = []

    for index, item in enumerate(items, start=1):
        page = item.get("page")
        page_label = (
            str(page + 1)
            if isinstance(page, int)
            else "unknown"
        )

        sections.append(
            f"""Context {index}
Source: {item.get("source_file") or "PDF"}
Page: {page_label}
Text:
{item["content"]}"""
        )

    return {
        "context_items": items,
        "context_text": "\n\n---\n\n".join(sections)
    }


def answer_node(state: PDFQuestionState) -> PDFQuestionState:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_CHAT_MODEL,
        temperature=0,
        google_api_key=settings.GEMINI_API_KEY
    )

    user_prompt = f"""
PDF CONTEXT:
{state.get("context_text", "")}

USER QUESTION:
{state["question"]}
""".strip()

    response = llm.invoke([
        SystemMessage(content=PDF_QA_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ])

    return {
        "answer": response.content
    }


def build_pdf_qa_graph():
    builder = StateGraph(PDFQuestionState)

    builder.add_node("retrieve_pdf_context", retrieve_node)
    builder.add_node("answer_from_pdf", answer_node)

    builder.add_edge(START, "retrieve_pdf_context")
    builder.add_edge("retrieve_pdf_context", "answer_from_pdf")
    builder.add_edge("answer_from_pdf", END)

    return builder.compile()


pdf_qa_graph = build_pdf_qa_graph()


def ask_pdf(user_id: str, question: str) -> dict:
    result = pdf_qa_graph.invoke({
        "user_id": user_id,
        "question": question
    })

    return {
        "answer": result["answer"],
        "sources": [
            {
                "source_file": item.get("source_file"),
                "page": (
                    item["page"] + 1
                    if isinstance(item.get("page"), int)
                    else None
                )
            }
            for item in result.get("context_items", [])
        ]
    }
