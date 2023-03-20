from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/patient-data/")
async def patient_data(file: UploadFile = File(...)) -> JSONResponse:
    pass
