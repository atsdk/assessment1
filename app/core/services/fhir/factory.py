from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from app.core.services.fhir.models import (
    AllergyIntolerance, CarePlan, CareTeam, Claim, Condition, Device,
    DiagnosticReport, DocumentReference, Encounter, ExplanationOfBenefit,
    ImagingStudy, Immunization, Medication, MedicationAdministration,
    MedicationRequest, Observation, Patient, Procedure, Provenance,
    SupplyDelivery,
)
from app.core.services.fhir.migrator import (
    BaseMigrator,
    PatientAllergyIntoleranceMigrator,
)
from app.core.exceptions.fhir import InvalidFHIRResourceException

if TYPE_CHECKING:
    from app.core.services.fhir.models import FHIRModel

logger = logging.getLogger(__name__)


MODEL_MAPPING = {
    "AllergyIntolerance": AllergyIntolerance,
    "CarePlan": CarePlan,
    "CareTeam": CareTeam,
    "Claim": Claim,
    "Condition": Condition,
    "Device": Device,
    "DiagnosticReport": DiagnosticReport,
    "DocumentReference": DocumentReference,
    "Encounter": Encounter,
    "ExplanationOfBenefit": ExplanationOfBenefit,
    "ImagingStudy": ImagingStudy,
    "Immunization": Immunization,
    "Medication": Medication,
    "MedicationAdministration": MedicationAdministration,
    "MedicationRequest": MedicationRequest,
    "Observation": Observation,
    "Patient": Patient,
    "Procedure": Procedure,
    "Provenance": Provenance,
    "SupplyDelivery": SupplyDelivery,
}


MIGRATOR_MAPPING = {
    "AllergyIntolerance": PatientAllergyIntoleranceMigrator,
}


def get_model(resource_type: str) -> FHIRModel:
    """Get a model class for a given resource type."""
    if not (model := MODEL_MAPPING.get(resource_type)):
        logger.error("Invalid resource type: %s", resource_type)
        raise InvalidFHIRResourceException()
    return model


def get_migrator(resource_type: str) -> BaseMigrator:
    """Get a migrator class for a given resource type."""
    # Just for the sake of test
    return MIGRATOR_MAPPING.get(resource_type)
