from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core import settings

engine = create_engine(
    settings.database_uri,
    convert_unicode=True,
    **settings.database_connect_options
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def init_db():
    Model.metadata.create_all(bind=engine)


Model = declarative_base(name="Model")
Model.query = db_session.query_property()


class FHIRModel(Model):
    __abstract__ = True
    id = Column("id", String, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    resource = Column(JSON)


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
