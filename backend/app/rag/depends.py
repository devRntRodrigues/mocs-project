from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.rag.service import LangChainRAGService


def get_rag_service() -> LangChainRAGService:
    return LangChainRAGService()


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
RAGServiceDep = Annotated[LangChainRAGService, Depends(get_rag_service)]
