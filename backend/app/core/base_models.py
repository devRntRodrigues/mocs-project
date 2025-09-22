from __future__ import annotations

from pydantic import BaseModel, ConfigDict

STANDARD_CONFIG = ConfigDict(
    str_strip_whitespace=True,
    validate_default=True,
    extra="forbid",
)

DATABASE_CONFIG = ConfigDict(
    str_strip_whitespace=True,
    validate_default=True,
    extra="forbid",
    from_attributes=True,
)


class BaseSchema(BaseModel):
    model_config = STANDARD_CONFIG


class BaseDatabaseSchema(BaseModel):
    model_config = DATABASE_CONFIG
