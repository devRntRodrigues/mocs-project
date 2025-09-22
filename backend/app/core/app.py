from __future__ import annotations

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.core.config import settings


def include_routes(fastapi: FastAPI) -> None:
    from app.routers import include_all_routers

    include_all_routers(fastapi)


def get_application() -> FastAPI:
    from fastapi import FastAPI
    from starlette.middleware.cors import CORSMiddleware

    from app.core.db import close_database_connection, connect_database

    fastapi = FastAPI(
        title="Document Processor API",
        version="1.0.0",
        swagger_ui_parameters={
            "docExpansion": "none",
            "operationsSorter": "alpha",
            "tagsSorter": "alpha",
        },
    )

    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi.add_event_handler("startup", connect_database)
    fastapi.add_event_handler("shutdown", close_database_connection)

    include_routes(fastapi)
    add_pagination(fastapi)

    return fastapi
