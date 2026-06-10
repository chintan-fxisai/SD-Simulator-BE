from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool = True
    message: str
    data: DataT | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: list[dict[str, object]] = Field(default_factory=list)


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


class PaginatedResponse(BaseModel, Generic[DataT]):
    items: list[DataT]
    total: int
    page: int
    page_size: int


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
