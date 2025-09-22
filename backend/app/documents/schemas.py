from __future__ import annotations

from datetime import datetime

from app.core.base_models import BaseSchema


class DocumentProcessingResult(BaseSchema):
    document_id: int
    chunks_created: int
    processing_time_ms: int
    status: str
    processed_at: datetime


class RAGProcessingResult(BaseSchema):
    chunks_created: int
    rag_processing_time_ms: int
    status: str


class DocumentUploadResult(BaseSchema):
    id: int
    file_name: str
    text_content: str
    text_length: int
    processing_time_ms: int
    created_at: datetime
    rag_processing: RAGProcessingResult


class DocumentDetail(BaseSchema):
    id: int
    file_name: str
    text_content: str
    created_at: datetime
    updated_at: datetime | None


class DocumentSummary(BaseSchema):
    id: int
    file_name: str
    text_length: int
    created_at: datetime


class DocumentDeleteResult(BaseSchema):
    deleted: bool
