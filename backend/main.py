"""Main entry point for the FastAPI application."""

from __future__ import annotations

import uvicorn

from app.core.app import get_application
from app.core.config import settings


def main():
    """Run the FastAPI application."""
    if settings.app.debug:
        # Use import string for reload to work properly
        uvicorn.run(
            "app.core.app:get_application",
            host="0.0.0.0",
            port=8000,
            reload=True,
            factory=True,
        )
    else:
        # Production mode - use app instance directly
        app = get_application()
        uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
