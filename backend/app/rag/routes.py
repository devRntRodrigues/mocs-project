from __future__ import annotations

from fastapi import APIRouter

from app.core.response_patterns import APIResponse, create_response
from app.rag.depends import RAGServiceDep
from app.rag.schemas import (
    QuestionRequest,
    RAGQuestionResponse,
)

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/question", response_model=APIResponse[RAGQuestionResponse])
async def ask_question(
    request: QuestionRequest,
    service: RAGServiceDep,
) -> APIResponse[RAGQuestionResponse]:
    result = await service.ask_question(
        question=request.question, document_id=request.document_id, max_chunks=request.max_chunks
    )

    return create_response(
        data=result, message="Question processed successfully with LangChain RAG"
    )
