from __future__ import annotations

import logging
import os

from typing import TYPE_CHECKING, List, Optional

from app.core import settings
from app.core.exceptions.file import (
    InvalidFileExtensionException,
    InvalidFilenameLengthException,
    InvalidFileSizeException,
)

if TYPE_CHECKING:
    from fastapi import UploadFile


logger = logging.getLogger(__name__)


def get_data_file_destination(filename: str) -> str:
    """Returns the path to the data directory."""
    return os.path.join(settings.root_dir, settings.data_dir, filename)


def validate_file(
    file: UploadFile, allowed_content_types: Optional[List[str]] = None,
) -> None:
    """Validates the file."""
    if not allowed_content_types:
        allowed_content_types = settings.allowed_content_types

    if extension := file.filename.split(".")[-1] not in allowed_content_types:
        logger.error(
            "File %s has invalid extension %s", file.filename, extension,
        )
        raise InvalidFileExtensionException()
    if file.size > settings.max_file_size:
        logger.error(
            "File %s size %s exceeds max file size %s",
            file.filename,
            file.size,
            settings.max_file_size,
        )
        raise InvalidFileSizeException()
    if not settings.max_filename_length > len(file.filename) > 0:
        logger.error(
            "File %s name length %s exceeds max filename length %s",
            file.filename,
            len(file.filename),
            settings.max_filename_length,
        )
        raise InvalidFilenameLengthException()
    # TODO: Add more validations
    # like check whether the file is actually of type it is supposed to be
    # or the name contains any invalid characters,etc.
