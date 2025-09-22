from __future__ import annotations

import asyncio

from langchain_openai import OpenAIEmbeddings
from loguru import logger

from app.core.config import settings


class LangChainEmbeddingsService:
    def __init__(self) -> None:
        api_key = settings.openai.api_key.get_secret_value()
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model=settings.openai.embedding_model,
        )

        self.embedding_model = settings.openai.embedding_model

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        all_embeddings = []
        batch_size = 100

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            batch_embeddings = await self.embeddings.aembed_documents(batch)
            all_embeddings.extend(batch_embeddings)

            if i + batch_size < len(texts):
                await asyncio.sleep(0.1)

        logger.info(f"Generated embeddings for {len(texts)} texts using LangChain")
        return all_embeddings

    async def generate_query_embedding(self, query: str) -> list[float]:
        embedding = await self.embeddings.aembed_query(query)
        logger.info("Generated query embedding using LangChain")
        return embedding
