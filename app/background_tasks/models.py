from sqlalchemy import (
    Column,
    String,
    Index,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.database import Model


class CeleryFHIRMigration(Model):
    __tablename__ = "celery_fhir_migration"
    __table_args__ = (
        Index(
            "celery_fhir_migration_file_name_last_modified_idx",
            "file_name",
            "date_last_modified",
            unique=True,
        ),
    )

    file_name = Column(String, primary_key=True)
    date_last_modified = Column(TIMESTAMP, nullable=False)
    # Would be better to track migration status in the celery task
