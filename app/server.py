from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.middlewares import AuthenticationMiddleware


def make_middleware() -> List[Middleware]:
    middleware = [
        # Just an example default middleware
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # Custom middleware we use for Authentication for all of app routes
        Middleware(AuthenticationMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="EMIS Group Data Engineer Technical Assesment",
        description=(
            "Application to receive a patient data from "
            "external system/supplier and transform it into "
            "more workeable for analytics team format."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    app_.include_router(router)
    return app_


app = create_app()
