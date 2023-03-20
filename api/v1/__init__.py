from fastapi import APIRouter

from api.v1.patient_data import router as patient_data_router


router = APIRouter()
router.include_router(patient_data_router)


__all__ = ["router"]
