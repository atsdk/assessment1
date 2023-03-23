import logging

from celery import current_app as current_celery_app
from celery import Task

from app.core import settings
from app.core.services.fhir.data_migration import (
    save_file_to_db_only_complex_model,
    save_file_to_db_simple_model,
)
from app.database import session

celery_app = current_celery_app
celery_app.conf.update(broker_url=settings.celery_broker_uri)

logger = logging.getLogger(__name__)


class DBTask(Task):
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.remove()

    @property
    def session(self):
        if self._session is None:
            self._session = session

        return self._session

# To be honest, I cannot register this task outside of this file
# so be it for now


@celery_app.task(bind=True, base=DBTask)
def migrate_file_from_fhir_to_sql(self, path: str) -> None:
    try:
        save_file_to_db_simple_model(self.session, path)
        save_file_to_db_only_complex_model(self.session, path)
    except Exception as e:
        logger.error(
            "File %s processing error: %s", path, e,
            exc_info=True
        )


# Should add scheduled task to migrate all files in the directory
