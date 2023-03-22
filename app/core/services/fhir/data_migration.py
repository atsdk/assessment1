from __future__ import annotations
# Use ijson in order to parse the file in a memory-efficient way
# might be useful for large files
import ijson
import logging
from typing import TYPE_CHECKING

from app.core.services.fhir.mapping import MAPPING
from app.core.exceptions.fhir import InvalidFHIRResourceException

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def _save_file_to_db_easy_way(session: Session, path: str) -> None:
    """Parse the file and save FHIR resources to the database."""
    with open(path, "rb") as f:
        # Add check whether it's bundle or a resource
        # and treat it accordingly
        for entry in ijson.items(f, "entry.item", use_float=True):
            resource_type = entry["resource"]["resourceType"]
            if not (model := MAPPING.get(resource_type)):
                logger.error("Unknown resource type: %s", resource_type)
                raise InvalidFHIRResourceException()
            obj = model(id=entry["resource"]["id"], resource=entry["resource"])
            session.merge(obj)
            # use bulk insert
            session.commit()
