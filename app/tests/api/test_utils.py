import io

import pytest
from fastapi import UploadFile

from app.api.utils import validate_file

from app.core.exceptions.file import (
    InvalidFileExtensionException,
    InvalidFilenameLengthException,
    InvalidFileSizeException,
)


@pytest.fixture
def file():
    """Factory for creating a file fixture."""

    def _file(filename: str = "test.txt", size: int = 1024):
        return UploadFile(
            file=io.BytesIO(b"test"),
            filename=filename,
            size=size,
        )

    return _file


@pytest.fixture
def settings(mocker):
    """Returns the settings."""
    return mocker.patch(
        "app.api.utils.settings",
        allowed_content_types=["txt"],
        max_file_size=1024,
        max_filename_length=10,
    )


def test_validate_file_success(file, settings):
    """Test that the file is validated successfully."""

    validate_file(file())


def test_validate_file_explicit_allowed_content_types_success(file, settings):
    """Test that the file is validated against th explicit passed
    allowed content types.
    """
    validate_file(file(), allowed_content_types=["txt"])


def test_validate_file_invalid_extension(file, settings):
    """Test that the validation fails when the file has an invalid
    extension.
    """

    with pytest.raises(InvalidFileExtensionException):
        validate_file(file(filename="test.json"))


def test_validate_file_invalid_size(file, settings):
    """Test that the validation fails when the file size is invalid."""

    with pytest.raises(InvalidFileSizeException):
        validate_file(file(size=1025))


def test_validate_file_invalid_filename_length(file, settings):
    """Test that the validation fails when the file name length is invalid."""

    with pytest.raises(InvalidFilenameLengthException):
        validate_file(file(filename="testtesttest.txt"))
