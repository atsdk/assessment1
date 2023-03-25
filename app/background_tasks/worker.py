from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from celery import current_app as current_celery_app
from celery import Task

from app.core import settings
from app.core.services.fhir.data_migration import (
    save_file_to_db_only_complex_model,
    save_file_to_db_simple_model,
)
from app.database import Session

if TYPE_CHECKING:
    from sqlalchemy.orm import Session as SessionType

celery_app = current_celery_app
celery_app.conf.update(broker_url=settings.celery_broker_uri)

logger = logging.getLogger(__name__)


class DBTask(Task):
    """Task class that provides a session management for the task.
    """
    _session = None

    def after_return(self, *args, **kwargs) -> None:
        if self._session is not None:
            self._session.remove()

    @property
    def session(self) -> SessionType:
        if self._session is None:
            self._session = Session

        return self._session


@celery_app.task(bind=True, base=DBTask)
def migrate_file_from_fhir_to_sql(self, path: str) -> None:
    """Background task that migrates the file by path from FHIR to SQL."""
    try:
        save_file_to_db_simple_model(self.session, path)
        save_file_to_db_only_complex_model(self.session, path)
    except Exception as e:
        logger.error(
            "File %s processing error: %s", path, e,
            exc_info=True
        )

# TODO: Add a task that will be called by the celery beat,
# will iterate through the files in the directory,
# check the file against some special data migration table
# and will call the task above for each file
