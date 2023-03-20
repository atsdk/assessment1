from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from core.settings import settings


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    # TODO: add return type
    async def dispatch(self, request: Request, call_next: Callable):
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, credentials = authorization.split(" ")
                if scheme.lower() == "bearer":
                    if (
                        settings.DEFAULT_AUTH_TOKEN
                        and credentials == settings.DEFAULT_AUTH_TOKEN
                    ):
                        return await call_next(request)
            except Exception as e:
                print(e)
                # logging

        return JSONResponse({"error": "Unauthenticated"}, status_code=401)
