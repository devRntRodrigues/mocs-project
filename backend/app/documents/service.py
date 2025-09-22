"""Serviço de documentos - simples e direto."""

from __future__ import annotations

import asyncio
import tempfile
import time
from pathlib import Path

import pytesseract
from fastapi import UploadFile
from loguru import logger
from pdf2image import convert_from_path
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.documents.models import Document
from app.documents.rag_processor import DocumentRAGProcessor
from app.documents.schemas import (
    DocumentDetail,
    DocumentProcessingResult,
    DocumentSummary,
    DocumentUploadResult,
    RAGProcessingResult,
)


class DocumentService:
    def __init__(self) -> None:
        self.upload_dir = Path(settings.app.upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.supported_formats = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
        self.rag_processor = DocumentRAGProcessor()

    async def upload_and_extract(self, file: UploadFile, db: AsyncSession) -> DocumentUploadResult:
        if not file.filename:
            logger.error("File name is required")
            raise ValueError("File name is required")

        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.supported_formats:
            logger.error(f"Format {file_ext} not supported")
            raise ValueError(f"Format {file_ext} not supported")

        file_path = self.upload_dir / file.filename
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

            start_time = time.perf_counter()
            text_content = await self._extract_text(file_path)
            processing_time = int((time.perf_counter() - start_time) * 1000)

            document = Document(
                file_name=file.filename,
                file_path=str(file_path),
                text_content=text_content,
            )
            db.add(document)
            await db.commit()
            await db.refresh(document)

            rag_result = await self.process_document_for_rag(int(document.id), text_content)

            return DocumentUploadResult(
                id=document.id,
                file_name=document.file_name,
                text_content=text_content,
                text_length=len(text_content),
                processing_time_ms=processing_time,
                created_at=document.created_at,
                rag_processing=RAGProcessingResult(
                    chunks_created=rag_result.chunks_created,
                    rag_processing_time_ms=rag_result.processing_time_ms,
                    status=rag_result.status,
                ),
            )

    async def process_document_for_rag(
        self, document_id: int, text_content: str
    ) -> DocumentProcessingResult:
        """Processar documento para RAG usando processor independente."""
        return await self.rag_processor.process_document(document_id, text_content)

    async def get_document(self, document_id: int, db: AsyncSession) -> DocumentDetail | None:
        result = await db.execute(select(Document).where(Document.id == document_id))
        doc = result.scalar_one_or_none()

        if not doc:
            return None

        return DocumentDetail(
            id=doc.id,
            file_name=doc.file_name,
            text_content=doc.text_content,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )

    async def list_documents(self, db: AsyncSession) -> list[DocumentSummary]:
        result = await db.execute(select(Document).order_by(Document.created_at.desc()))
        docs = result.scalars().all()

        return [
            DocumentSummary(
                id=doc.id,
                file_name=doc.file_name,
                text_length=len(doc.text_content),
                created_at=doc.created_at,
            )
            for doc in docs
        ]

    async def delete_document(self, document_id: int, db: AsyncSession) -> bool:
        result = await db.execute(select(Document).where(Document.id == document_id))
        doc = result.scalar_one_or_none()

        if not doc:
            return False

        await self.rag_processor.delete_document_chunks(document_id)

        file_path = Path(doc.file_path)
        if file_path.exists():
            file_path.unlink()

        await db.delete(doc)
        await db.commit()
        return True

    async def _extract_text(self, file_path: Path) -> str:
        if file_path.suffix.lower() == ".pdf":
            return await self._extract_from_pdf(file_path)
        else:
            return await self._extract_from_image(file_path)

    async def _extract_from_image(self, image_path: Path) -> str:
        loop = asyncio.get_event_loop()

        def _extract() -> str:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image, lang="por+eng")

        return await loop.run_in_executor(None, _extract)

    async def _extract_from_pdf(self, pdf_path: Path) -> str:
        loop = asyncio.get_event_loop()

        def _extract() -> str:
            images = convert_from_path(pdf_path)
            all_text = []

            for image in images:
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    image.save(temp_file.name, "PNG")
                    try:
                        text = pytesseract.image_to_string(image, lang="por+eng")
                        all_text.append(text.strip())
                    finally:
                        Path(temp_file.name).unlink()

            return "\n\n".join(all_text)

        return await loop.run_in_executor(None, _extract)
