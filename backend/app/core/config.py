from __future__ import annotations

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    url: str = "postgresql+asyncpg://admin:password123@localhost:5432/mocs_db"


class OpenAIConfig(BaseModel):
    api_key: SecretStr = Field(default=SecretStr(""))
    model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    max_tokens: int = 1000
    temperature: float = 0.1


class PGVectorConfig(BaseModel):
    table_name: str = "document_embeddings"
    embedding_dimension: int = 1536
    distance_metric: str = "cosine"


class AppConfig(BaseModel):
    debug: bool = True
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    cors_origins: list[str] = ["http://localhost:3000"]


class Settings(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()

    openai: OpenAIConfig = OpenAIConfig()

    pgvector: PGVectorConfig = PGVectorConfig()

    app: AppConfig = AppConfig()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


settings = Settings()
