import logging
import shutil

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from app.core import settings
from app.core.exceptions.file import FileProcessingException

from app.api.models import ErrorBase, FileResponseBase
from app.api.utils import get_data_file_destination, validate_file

router = APIRouter(responses={400: {"model": ErrorBase}})
logger = logging.getLogger(__name__)


@router.post("/patient-data/", response_model=FileResponseBase)
def patient_data(file: UploadFile) -> JSONResponse:
    """Receives, validates and uploads patient data file to the server."""
    validate_file(file, ["json"])

    destination_file_path = get_data_file_destination(file.filename)
    try:
        # TODO: Add a check to see if the file already exists
        with open(destination_file_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file, settings.file_chunk_size)
    except Exception as e:
        logger.error(
            "File %s processing error: %s", file.filename, e, exc_info=True
        )
        raise FileProcessingException from e

    from app.background_tasks.worker import migrate_data_files_from_fhir_to_sql
    migrate_data_files_from_fhir_to_sql.delay()

    return JSONResponse(
        status_code=200,
        content={
            "message": "File uploaded successfully.",
            "filename": file.filename,
        },
    )
