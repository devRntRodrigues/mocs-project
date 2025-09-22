from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from langchain.chains import RetrievalQA
from loguru import logger

from app.core.vector_store import LangChainPGVectorService
from app.rag.embeddings import LangChainEmbeddingsService
from app.rag.llm import LangChainLLMService
from app.rag.schemas import (
    DocumentDeleteResult,
    RAGQuestionResponse,
    SourceChunk,
)


class LangChainRAGService:
    def __init__(self) -> None:
        self.llm_service = LangChainLLMService()
        self.embeddings_service = LangChainEmbeddingsService()
        self.vector = LangChainPGVectorService(self.embeddings_service.embeddings)

    async def ask_question(
        self, question: str, document_id: int | None = None, max_chunks: int = 3
    ) -> RAGQuestionResponse:
        return await self.ask_question_with_qa_chain(question, document_id, max_chunks)

    async def delete_document_data(self, document_id: int) -> DocumentDeleteResult:
        deleted_count = await self.vector.delete_document_chunks(document_id)

        return DocumentDeleteResult(
            document_id=document_id,
            chunks_deleted=deleted_count,
            status="success",
        )

    async def create_retrieval_qa_chain(
        self, document_id: int | None = None, max_chunks: int = 3
    ) -> RetrievalQA:
        await self.vector.initialize()

        retriever_kwargs: dict[str, Any] = {"k": max_chunks}
        if document_id is not None:
            retriever_kwargs["filter"] = {"document_id": document_id}

        retriever = self.vector.as_retriever(**retriever_kwargs)

        from app.rag.prompts import get_rag_prompt

        enhanced_prompt = get_rag_prompt()

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm_service.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": enhanced_prompt},
        )

        return qa_chain

    async def ask_question_with_qa_chain(
        self, question: str, document_id: int | None = None, max_chunks: int = 3
    ) -> RAGQuestionResponse:
        start_time = time.perf_counter()

        qa_chain = await self.create_retrieval_qa_chain(document_id, max_chunks)

        result = qa_chain({"query": question})

        processing_time = int((time.perf_counter() - start_time) * 1000)

        source_chunks = [
            SourceChunk(
                content=doc.page_content,
                document_id=doc.metadata.get("document_id", 0),
                chunk_id=doc.metadata.get("chunk_id", 0),
                source=doc.metadata.get("source"),
            )
            for doc in result.get("source_documents", [])
        ]

        logger.info(f"LangChain RAG processed question with {len(source_chunks)} source chunks")

        return RAGQuestionResponse(
            question=question,
            answer=result["result"],
            source_chunks=source_chunks,
            processing_time_ms=processing_time,
            method="langchain_retrieval_qa",
            created_at=datetime.now(),
        )
