from __future__ import annotations

import logging
import os

from collections import defaultdict
from typing import TYPE_CHECKING
# Use ijson in order to parse the file in a memory-efficient way
# might be useful for large files
import ijson
import orjson

from app.core.services.fhir.factory import get_model, get_migrator
from app.core import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def save_file_to_db_only_complex_model(session: Session, path: str) -> None:
    """Parse the file and save FHIR resources to the database."""
    if not os.path.exists(path):
        logger.error("File %s does not exist", path)
        raise FileNotFoundError()
    # TODO: check whether it's bundle or a resource
    # and treat it accordingly, but for now we gonna
    # assume that all files are bundles
    # TODO: handle exceptions
    with open(path, "rb") as file:
        for entry in ijson.items(file, "entry.item", use_float=True):
            resource = entry["resource"]
            if migrator := get_migrator(resource["resourceType"]):
                migrator.migrate(resource, session)


def save_file_to_db_simple_model(session: Session, path: str) -> None:
    """Parse the file and save FHIR resources to the database."""
    if not os.path.exists(path):
        logger.error("File %s does not exist", path)
        raise FileNotFoundError()
    # TODO: check whether it's bundle or a resource
    # and treat it accordingly, but for now we gonna
    # assume that all files are bundles
    # TODO: handle exceptions
    if os.path.getsize(path) > settings.max_single_read_file_size:
        _migrate_large_file_simple_model(session, path)
    else:
        _migrate_small_file_simple_model(session, path)


def _migrate_large_file_simple_model(session: Session, path: str) -> None:
    """Iterate through the file with memory-efficient ijson lib
    and save the resources to the database one by one
    """
    # TODO: some kind of chunks too
    with open(path, "rb") as file:
        for entry in ijson.items(file, "entry.item", use_float=True):
            resource_type = entry["resource"]["resourceType"]
            model = get_model(resource_type)
            obj = model(id=entry["resource"]["id"], resource=entry["resource"])
            session.merge(obj)
            session.commit()


def _migrate_small_file_simple_model(session: Session, path: str) -> None:
    """Read the whole file into memory and save the resources
    to the database in chunks
    """
    result = defaultdict()

    with open(path, "rb") as file:
        data = orjson.loads(file.read())
        for entry in data["entry"]:
            resource_type = entry["resource"]["resourceType"]
            model = get_model(resource_type)
            obj = model(id=entry["resource"]["id"], resource=entry["resource"])
            result[model][entry["resource"]["id"]] = obj
    # Upsert already existing objects
    for model, objects in result.items():
        for each in model.query.filter(model.id.in_(objects.keys())):
            session.merge(objects.pop(str(each.id)))
    # Bulk insert new objects
    all_objects = []
    for obj in result.values():
        all_objects.extend(list(obj.values()))
    session.add_all(all_objects)

    session.commit()
