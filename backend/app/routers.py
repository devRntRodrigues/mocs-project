"""Routers centralizados da aplicação."""

from fastapi import FastAPI

from app.documents.routes import router as documents_router
from app.rag.routes import router as rag_router


def include_all_routers(app: FastAPI) -> None:
    app.include_router(documents_router)
    app.include_router(rag_router)
