from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.common import ErrorResponse


class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: list[dict[str, object]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class PermissionDeniedException(AppException):
    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Validation failed",
        errors: list[dict[str, object]] | None = None,
    ) -> None:
        super().__init__(
            message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=errors,
        )


def _error_response(
    message: str,
    status_code: int,
    errors: list[dict[str, object]] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(message=message, errors=errors or []).model_dump(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    def normalize_errors(errors: list[dict[str, object]]) -> list[dict[str, object]]:
        return [
            {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"],
            }
            for error in errors
        ]

    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        return _error_response(exc.message, exc.status_code, exc.errors)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return _error_response(
            "Validation failed",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=normalize_errors(exc.errors()),
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
        return _error_response(
            "Validation failed",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=normalize_errors(exc.errors()),
        )
