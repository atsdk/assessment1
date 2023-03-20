from core.exceptions.base import CoreException


class FileException(CoreException):
    """Base class for file exceptions."""


class InvalidFileSizeException(FileException):
    """Raised when the file size is invalid."""


class InvalidFileExtensionException(FileException):
    """Raised when the file extension is invalid."""


class InvalidFilenameLengthException(FileException):
    """Raised when the file name length is invalid."""


class FileProcessingException(FileException):
    """Raised when the file processing fails."""
