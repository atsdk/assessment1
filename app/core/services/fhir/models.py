# TODO: move it out of business logic
# because it contains details (database model)
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Model


class FHIRModel(Model):
    """This is not actualy needed in this case. We can use raw SQL inserts.
    But:
    1) It is better protected against SQL injections.
    2) It is a convenient way to init database.
    3) Provides flexibility to use some of this models inside the app later.
    """
    __abstract__ = True
    id = Column(String, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    resource = Column(JSONB)
    # If we every will want to use this models in the app
    # better to use sqlalchemy-json, so we are able to change fields inplace


class AllergyIntolerance(FHIRModel):
    __tablename__ = "allergy_intolerance"


class CarePlan(FHIRModel):
    __tablename__ = "care_plan"


class CareTeam(FHIRModel):
    __tablename__ = "care_team"


class Claim(FHIRModel):
    __tablename__ = "claim"


class Condition(FHIRModel):
    __tablename__ = "condition"


class Device(FHIRModel):
    __tablename__ = "device"


class DiagnosticReport(FHIRModel):
    __tablename__ = "diagnostic_report"


class DocumentReference(FHIRModel):
    __tablename__ = "document_reference"


class Encounter(FHIRModel):
    __tablename__ = "encounter"


class ExplanationOfBenefit(FHIRModel):
    __tablename__ = "explanation_of_benefit"


class ImagingStudy(FHIRModel):
    __tablename__ = "imaging_study"


class Immunization(FHIRModel):
    __tablename__ = "immunization"


class Medication(FHIRModel):
    __tablename__ = "medication"


class MedicationAdministration(FHIRModel):
    __tablename__ = "medication_administration"


class MedicationRequest(FHIRModel):
    __tablename__ = "medication_request"


class Observation(FHIRModel):
    __tablename__ = "observation"


class Patient(FHIRModel):
    __tablename__ = "patient"


class Procedure(FHIRModel):
    __tablename__ = "procedure"


class Provenance(FHIRModel):
    __tablename__ = "provenance"


class SupplyDelivery(FHIRModel):
    __tablename__ = "supply_delivery"
