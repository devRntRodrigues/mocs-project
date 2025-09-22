from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.core.base_models import BaseSchema


class SourceChunk(BaseSchema):
    content: str
    document_id: int
    chunk_id: int
    source: str | None


class RAGQuestionRequest(BaseSchema):
    question: str
    document_id: int | None
    max_chunks: int
    use_qa_chain: bool


class RAGQuestionResponse(BaseSchema):
    question: str
    answer: str
    source_chunks: list[SourceChunk]
    processing_time_ms: int
    method: str
    created_at: datetime


class DocumentDeleteResult(BaseSchema):
    document_id: int
    chunks_deleted: int
    status: str


class RAGStats(BaseSchema):
    total_chunks: int
    total_documents: int
    table_name: str
    embedding_dimension: int
    error: str | None


class VectorSearchResult(BaseSchema):
    document_id: int
    chunk_id: int
    content: str
    distance: float
    relevance_score: float


class PromptConfiguration(BaseSchema):
    prompt_type: str
    system_message: str
    user_template: str
    temperature: float
    max_tokens: int


class QuestionRequest(BaseModel):
    question: str
    document_id: int | None = None
    max_chunks: int = 3
