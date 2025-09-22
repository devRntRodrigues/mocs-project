from __future__ import annotations

import asyncio
from typing import Any

from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from loguru import logger

from app.core.config import settings


class LangChainPGVectorService:
    def __init__(self, embedding_function: Embeddings) -> None:
        self.table_name = settings.pgvector.table_name
        self.embedding_dimension = settings.pgvector.embedding_dimension
        self.distance_metric = settings.pgvector.distance_metric
        self.embedding_function = embedding_function

        async_url = settings.database.url
        self.connection_string = async_url.replace("postgresql+asyncpg://", "postgresql://")

        self.vector_store: PGVector | None = None
        self._initialized = False

    async def initialize(self) -> None:
        if self._initialized:
            return

        def _create_pgvector() -> PGVector:
            from langchain_community.vectorstores.pgvector import DistanceStrategy

            return PGVector(
                connection_string=self.connection_string,
                embedding_function=self.embedding_function,
                collection_name=self.table_name,
                distance_strategy=DistanceStrategy.COSINE,
                pre_delete_collection=False,
            )

        self.vector_store = await asyncio.get_event_loop().run_in_executor(None, _create_pgvector)

        self._initialized = True
        logger.info(f"LangChain PGVector initialized with table: {self.table_name}")

    async def add_document_chunks(self, document_id: int, chunks: list[str]) -> None:
        await self.initialize()

        documents = []
        for chunk_id, chunk_text in enumerate(chunks):
            doc = Document(
                page_content=chunk_text,
                metadata={
                    "document_id": document_id,
                    "chunk_id": chunk_id,
                    "source": f"document_{document_id}_chunk_{chunk_id}",
                },
            )
            documents.append(doc)

        def _add_documents() -> list[str]:
            if self.vector_store is None:
                raise RuntimeError("Vector store not initialized")
            return self.vector_store.add_documents(documents)

        await asyncio.get_event_loop().run_in_executor(None, _add_documents)

        logger.info(f"Added {len(chunks)} chunks for document {document_id} using LangChain")

    async def search_similar(
        self, query: str, document_id: int | None = None, limit: int = 5
    ) -> list[dict]:
        await self.initialize()

        filter_kwargs = {}
        if document_id is not None:
            filter_kwargs["filter"] = {"document_id": document_id}

        def _search() -> Any:
            if self.vector_store is None:
                raise RuntimeError("Vector store not initialized")
            return self.vector_store.similarity_search_with_score(query, k=limit, **filter_kwargs)

        docs_and_scores = await asyncio.get_event_loop().run_in_executor(None, _search)

        results = []
        for doc, score in docs_and_scores:
            results.append(
                {
                    "document_id": doc.metadata.get("document_id"),
                    "chunk_id": doc.metadata.get("chunk_id"),
                    "content": doc.page_content,
                    "distance": score,
                    "relevance_score": 1 - score,
                }
            )

        logger.info(f"Found {len(results)} similar chunks using LangChain")
        return results

    async def delete_document_chunks(self, document_id: int) -> int:
        await self.initialize()

        from sqlalchemy import create_engine, text

        engine = create_engine(self.connection_string)

        with engine.begin() as conn:
            result = conn.execute(
                text(
                    f"DELETE FROM {self.table_name} WHERE cmetadata->>'document_id' = :document_id"
                ),
                {"document_id": str(document_id)},
            )
            deleted_count = result.rowcount or 0

        logger.info(f"Deleted {deleted_count} chunks for document {document_id}")
        return deleted_count

    async def get_stats(self) -> dict[str, Any]:
        await self.initialize()

        from sqlalchemy import create_engine, text

        engine = create_engine(self.connection_string)

        stats_sql = f"""
            SELECT 
                COUNT(*) as total_chunks,
                COUNT(DISTINCT cmetadata->>'document_id') as total_documents
            FROM {self.table_name};
        """

        with engine.begin() as conn:
            result = conn.execute(text(stats_sql))
            row = result.fetchone()

        return {
            "total_chunks": row.total_chunks if row else 0,
            "total_documents": row.total_documents if row else 0,
            "table_name": self.table_name,
            "embedding_dimension": self.embedding_dimension,
        }

    async def close(self) -> None:
        pass

    def as_retriever(self, **kwargs: Any) -> Any:
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")
        return self.vector_store.as_retriever(**kwargs)
