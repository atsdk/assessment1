from app.core.exceptions.file import (
    InvalidFileExtensionException,
    InvalidFilenameLengthException,
    InvalidFileSizeException,
)

# Can be system-wide, can be api specific
ERRORS = {
    InvalidFilenameLengthException: dict(
        # We definitely want to obtain some data from the exception itself
        # like filename, in this case
        status_code=400, content={"error": "File name is too long"}
    ),
    InvalidFileSizeException: dict(
        status_code=400, content={"error": "File size is too big"}
    ),
    InvalidFileExtensionException: dict(
        status_code=400, content={"error": "File extension is invalid"}
    ),
}
