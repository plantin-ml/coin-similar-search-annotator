from typing import List, Union

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


def form_error_message(errors: List[dict]) -> List[str]:
    """
    Make valid pydantic `ValidationError` messages list.
    """

    messages = []
    for error in errors:
        field, message = error["loc"][-1], error["msg"]
        messages.append(f"`{field}` {message}")
    return messages


class BaseInternalException(Exception):
    """
    Base error class for inherit all internal errors.
    """

    def __init__(
        self, message: str, status_code: int, errors: List[Union[str, None]] = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors


class TaskNotFoundException(BaseInternalException):
    """
    Exception raised when `task_id` field from JSON body not found.
    """


class JobNotFoundException(BaseInternalException):
    """
    Exception raised when `alias` field from JSON body not found.
    """


def add_internal_exception_handler(app: FastAPI) -> None:
    """
    Handle all internal exceptions.
    """

    @app.exception_handler(BaseInternalException)
    async def _exception_handler(
        _: Request, exc: BaseInternalException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "type": type(exc).__name__,
                "message": exc.message,
                "errors": exc.errors or [],
            },
        )


def add_request_exception_handler(app: FastAPI) -> None:
    """
    Handle request validation errors exceptions.
    """

    @app.exception_handler(RequestValidationError)
    async def _exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "status": 422,
                "type": "RequestValidationError",
                "message": "Schema validation error",
                "errors": form_error_message(errors=exc.errors()),
            },
        )


def add_http_exception_handler(app: FastAPI) -> None:
    """Handle http exceptions."""

    @app.exception_handler(HTTPException)
    async def _exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "type": "HTTPException",
                "message": exc.detail,
                "errors": [],
            },
        )


def add_exception_handlers(app: FastAPI) -> None:
    """
    Set all exception handlers to app object.
    """

    add_internal_exception_handler(app=app)
    add_request_exception_handler(app=app)
    add_http_exception_handler(app=app)


class UserAlreadyExistException(BaseInternalException):
    """
    Exception raised when user try to log in with invalid username.
    """


class InvalidUserCredentialsException(BaseInternalException):
    """
    Exception raised when user try to log in with invalid credentials.
    """


class UserNotFoundException(BaseInternalException):
    """
    Exception raised when user try to register with already exist username.
    """
