import shutil

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from core import settings
from core.exceptions.file import FileProcessingException

from api.utils import get_data_file_destination, validate_file

router = APIRouter()


@router.post("/patient-data/")
def patient_data(file: UploadFile) -> JSONResponse:
    """Receives, validates and uploads patient data file to the server."""
    validate_file(file, ["json"])

    destination_file_path = get_data_file_destination(file.filename)
    try:
        # TODO: Add a check to see if the file already exists
        with open(destination_file_path, 'wb') as out_file:
            shutil.copyfileobj(file.file, out_file, settings.file_chunk_size)
    except Exception as e:
        raise FileProcessingException from e

    return JSONResponse(
        status_code=200,
        content={
            "message": "File uploaded successfully.",
            "filename": file.filename,
        },
    )
