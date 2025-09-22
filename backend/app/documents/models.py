from __future__ import annotations

from sqlalchemy import Column, String, Text

from app.core.db_model import PostgresBase


class Document(PostgresBase):
    __tablename__ = "documents"

    file_name = Column(String, nullable=False, index=True)
    file_path = Column(String, nullable=False)
    text_content = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name='{self.file_name}')>"
