from fastapi.responses import JSONResponse

from core.exceptions.file import (
    InvalidFileExtensionException,
    InvalidFilenameLengthException,
    InvalidFileSizeException,
)

# Can be system-wide, can be api specific
ERRORS = {
    InvalidFilenameLengthException: JSONResponse(
        status_code=400, content={"error": "File name is too long"}
    ),
    InvalidFileSizeException: JSONResponse(
        status_code=400, content={"error": "File size is too big"}
    ),
    InvalidFileExtensionException: JSONResponse(
        status_code=400, content={"error": "File extension is invalid"}
    ),
}
