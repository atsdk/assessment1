from __future__ import annotations

import os

from typing import TYPE_CHECKING, List, Optional

from core import settings
from core.exceptions.file import (
    InvalidFileExtensionException,
    InvalidFilenameLengthException,
    InvalidFileSizeException,
)

if TYPE_CHECKING:
    from fastapi import UploadFile


def get_data_file_destination(filename: str) -> str:
    """Returns the path to the data directory."""
    return os.path.join(settings.root_dir, settings.data_dir, filename)


def validate_file(
    file: UploadFile, allowed_content_types: Optional[List[str]] = None,
) -> None:
    """Validates the file."""
    if not allowed_content_types:
        allowed_content_types = settings.allowed_content_types

    if file.filename.split(".")[-1] not in allowed_content_types:
        raise InvalidFileExtensionException()
    if file.size > settings.max_file_size:
        raise InvalidFileSizeException()
    if not settings.max_filename_length > len(file.filename) > 0:
        raise InvalidFilenameLengthException()
    # TODO: Add more validations
    # like check whether the file is actually of type it is supposed to be
    # or the name contains any invalid characters,etc.
