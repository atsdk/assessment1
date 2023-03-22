from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, TYPE_CHECKING

from app.core.services.fhir.models import (
    Allergy, PatientAllergyIntolerance,
)

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class BaseMigrator(ABC):
    """Base class for all migrators"""
    @staticmethod
    @abstractmethod
    def migrate(resource: Dict[str, Any], session: Session) -> None:
        """Get a list of objects to be saved to the database"""
        raise NotImplementedError


class PatientAllergyIntoleranceMigrator(BaseMigrator):
    """Migrator for AllergyIntolerance resources"""
    @staticmethod
    def migrate(resource, session):
        coding = resource["code"]["coding"][0]
        session.merge(Allergy(code=coding["code"], display=coding["display"]))
        session.merge(
            PatientAllergyIntolerance(
                id=resource["id"],
                patient_id=resource["patient"]["reference"][9:],
                allergy_code=coding["code"],
                criticality=resource["criticality"],
                resource=resource,
            )
        )
        session.commit()
