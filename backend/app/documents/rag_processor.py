"""Processador RAG para documentos - sem dependências circulares."""

from __future__ import annotations

import time
from datetime import datetime

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from app.core.config import settings
from app.core.vector_store import LangChainPGVectorService
from app.documents.schemas import DocumentProcessingResult


class DocumentRAGProcessor:
    def __init__(self) -> None:
        api_key = settings.openai.api_key.get_secret_value()
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model=settings.openai.embedding_model,
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

        self.vector_store = LangChainPGVectorService(self.embeddings)

    async def process_document(
        self, document_id: int, text_content: str
    ) -> DocumentProcessingResult:
        start_time = time.perf_counter()

        chunks = self.text_splitter.split_text(text_content)

        if not chunks:
            raise ValueError("No chunks generated from document")

        logger.info(f"Generated {len(chunks)} chunks using LangChain text splitter")

        # Adicionar chunks ao vector store
        await self.vector_store.add_document_chunks(document_id, chunks)

        processing_time = int((time.perf_counter() - start_time) * 1000)

        return DocumentProcessingResult(
            document_id=document_id,
            chunks_created=len(chunks),
            processing_time_ms=processing_time,
            status="success",
            processed_at=datetime.now(),
        )

    async def delete_document_chunks(self, document_id: int) -> int:
        return await self.vector_store.delete_document_chunks(document_id)
