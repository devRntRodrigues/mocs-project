from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.documents.service import DocumentService


def get_document_service() -> DocumentService:
    return DocumentService()


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]
