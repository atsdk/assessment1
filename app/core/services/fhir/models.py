# TODO: move it out of business logic
# because it contains details (database model)
from datetime import datetime
from sqlalchemy import (
    BigInteger, Column, String, DateTime, Enum, ForeignKey, Index,
    text as sqlalchemy_text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Model

from app.core.services.fhir.enums import AllergyIntoleranceCriticality


class FHIRModel(Model):
    """This is not actualy needed in this case. We can use raw SQL inserts.
    But:
    1) It is better protected against SQL injections.
    2) It is a convenient way to init database.
    3) Provides flexibility to use some of this models inside the app later.
    """

    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    resource = Column(JSONB)
    # If we ever will want to use this models in the app
    # better to use sqlalchemy-json, so we are able to change fields inplace


class AllergyIntolerance(FHIRModel):
    __tablename__ = "allergy_intolerance"


class CarePlan(FHIRModel):
    __tablename__ = "care_plan"


class CareTeam(FHIRModel):
    __tablename__ = "care_team"


class Claim(FHIRModel):
    __tablename__ = "claim"
    __table_args__ = (
        Index(
            "claim_insurancetype_idx",
            sqlalchemy_text(
                "(resource#>'{insurance,0,coverage,display}') jsonb_path_ops"
            ),
            postgresql_using="gin",
        ),
    )


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


# Some examples on relational way to store data,
# full example would take a lot of time because of the complexity of the data
#
# This example shows, that we can pull any field we would query a lot
# out of the JSONB field and store it in a separate field
# connecting it to other tables via foreign keys
#
class Allergy(Model):
    __tablename__ = "allergy"

    code = Column(BigInteger, primary_key=True)
    display = Column(String(100), nullable=False)


class PatientAllergyIntolerance(FHIRModel):
    __tablename__ = "patient_allergy_intolerance"

    criticality = Column(Enum(AllergyIntoleranceCriticality))
    allergy = relationship("Allergy", backref="AllergyIntolerances")
    allergy_code = Column(BigInteger, ForeignKey("allergy.code"))
    patient = relationship("Patient", backref="AllergyIntolerances")
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patient.id"))
