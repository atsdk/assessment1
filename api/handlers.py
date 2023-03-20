from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from core.exceptions import CoreException

from api.errors import ERRORS


def error_handler(request: Request, error: CoreException) -> Response:
    """Handle error"""
    return ERRORS.get(
        error.__class__,
        JSONResponse(
            status_code=500,
            content={"error": "Unknown exception"}
        )
    )
