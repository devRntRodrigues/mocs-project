"""Simple API response patterns for our specific use cases."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class APIResponse[T](BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_default=True,
        extra="forbid",
    )

    success: Annotated[bool, Field(True, description="Operation success status")]
    data: Annotated[T, Field(description="Response data")]
    message: Annotated[str | None, Field(None, description="Optional success message")]
    request_id: Annotated[str, Field(description="Request tracking ID")]
    timestamp: Annotated[datetime, Field(description="Response timestamp")]


class ListResponse[T](BaseModel):
    """Response for list endpoints with simple pagination."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_default=True,
        extra="forbid",
    )

    success: Annotated[bool, Field(True, description="Operation success status")]
    data: Annotated[list[T], Field(description="Array of items")]
    count: Annotated[int, Field(description="Number of items returned")]
    request_id: Annotated[str, Field(description="Request tracking ID")]
    timestamp: Annotated[datetime, Field(description="Response timestamp")]


def create_response[T](
    data: T,
    message: str | None = None,
    request_id: str | None = None,
) -> APIResponse[T]:
    return APIResponse(
        success=True,
        data=data,
        message=message,
        request_id=request_id or str(uuid4()),
        timestamp=datetime.now(),
    )


def create_list_response[T](
    data: list[T],
    request_id: str | None = None,
) -> ListResponse[T]:
    return ListResponse(
        success=True,
        data=data,
        count=len(data),
        request_id=request_id or str(uuid4()),
        timestamp=datetime.now(),
    )
