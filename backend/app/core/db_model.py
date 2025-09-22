from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class PostgresBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
