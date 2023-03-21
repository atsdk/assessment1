from fastapi import APIRouter

from api.v1 import router as v1_router
from api.handlers import error_handler
from api.models import ErrorBase


router = APIRouter(responses={401: {"model": ErrorBase}})
router.include_router(v1_router, prefix="/api/v1", tags=["api-v1"])

__all__ = ["router"]
