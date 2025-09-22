from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.response_patterns import (
    APIResponse,
    ListResponse,
    create_list_response,
    create_response,
)
from app.documents.depends import DatabaseDep, DocumentServiceDep
from app.documents.schemas import (
    DocumentDeleteResult,
    DocumentDetail,
    DocumentSummary,
    DocumentUploadResult,
)
from app.rag.depends import RAGServiceDep
from app.rag.schemas import QuestionRequest, RAGQuestionResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=APIResponse[DocumentUploadResult])
async def upload_document(
    file: Annotated[UploadFile, File(..., description="File to upload")],
    db: DatabaseDep,
    service: DocumentServiceDep,
) -> APIResponse[DocumentUploadResult]:
    result = await service.upload_and_extract(file, db)
    return create_response(data=result, message="Document processed successfully")


@router.get("/", response_model=ListResponse[DocumentSummary])
async def list_documents(
    db: DatabaseDep,
    service: DocumentServiceDep,
) -> ListResponse[DocumentSummary]:
    documents = await service.list_documents(db)
    return create_list_response(data=documents)


@router.get("/{document_id}", response_model=APIResponse[DocumentDetail])
async def get_document(
    document_id: int,
    db: DatabaseDep,
    service: DocumentServiceDep,
) -> APIResponse[DocumentDetail]:
    document = await service.get_document(document_id, db)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return create_response(data=document, message="Document found")


@router.delete("/{document_id}", response_model=APIResponse[DocumentDeleteResult])
async def delete_document(
    document_id: int,
    db: DatabaseDep,
    service: DocumentServiceDep,
) -> APIResponse[DocumentDeleteResult]:
    deleted = await service.delete_document(document_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")

    return create_response(
        data=DocumentDeleteResult(deleted=True), message="Document deleted successfully"
    )


@router.post("/{document_id}/question", response_model=APIResponse[RAGQuestionResponse])
async def ask_document_question(
    document_id: int,
    request: QuestionRequest,
    service: RAGServiceDep,
) -> APIResponse[RAGQuestionResponse]:
    request.document_id = document_id

    result = await service.ask_question(
        question=request.question, document_id=document_id, max_chunks=request.max_chunks
    )

    return create_response(
        data=result, message=f"Question processed successfully for document {document_id}"
    )
