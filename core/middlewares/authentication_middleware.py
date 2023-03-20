from typing import List, Optional

from starlette import status
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import JSONResponse, Response

from core.settings import settings


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, route_prefixes: Optional[List[str]] = None
    ) -> None:
        super().__init__(app)
        self.route_prefixes = route_prefixes or []

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        scope = request.scope

        if not any(
            scope["path"].startswith(prefix) for prefix in self.route_prefixes
        ):
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if authorization:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() == "bearer":
                if (
                    settings.auth_token
                    and credentials == settings.auth_token
                ):
                    return await call_next(request)

        return JSONResponse(
            {"error": "Unauthenticated"}, status.HTTP_401_UNAUTHORIZED
        )
