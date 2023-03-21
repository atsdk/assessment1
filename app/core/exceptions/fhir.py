from app.core.exceptions.base import CoreException


class FHIRException(CoreException):
    """Base class for FHIR exceptions."""


class InvalidFHIRResourceException(FHIRException):
    """Raised when the FHIR resource is invalid."""
