from fastapi import FastAPI

from app.documents.routes import router as documents_router


def include_all_routers(app: FastAPI) -> None:
    app.include_router(documents_router)
