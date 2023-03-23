from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.exceptions import CoreException

from app.api.errors import ERRORS


def error_handler(_: Request, error: CoreException) -> Response:
    """Handle error"""
    error = ERRORS.get(
        error.__class__,
        {"status_code": 500, "content": {"error": "Unknown exception"}}
    )
    return JSONResponse(
        status_code=error["status_code"], content=error["content"]
    )
