from __future__ import annotations

from langchain_openai import ChatOpenAI
from loguru import logger

from app.core.config import settings


class LangChainLLMService:
    def __init__(self) -> None:
        api_key = settings.openai.api_key.get_secret_value()
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model=settings.openai.model,
            max_tokens=settings.openai.max_tokens,
            temperature=settings.openai.temperature,
        )

        logger.info(f"Initialized LangChain LLM with model: {settings.openai.model}")
