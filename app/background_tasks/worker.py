import os

from celery import Task
from celery import current_app as current_celery_app

from app.background_tasks.models import CeleryFHIRMigration
from app.core import settings
from app.database import get_session

celery_app = current_celery_app
celery_app.conf.update(broker_url=settings.celery_broker_uri)


class DBTask(Task):
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.remove()

    @property
    def session(self):
        if self._session is None:
            self._session = get_session()

        return self._session


# To be honest, I cannot register this task outside of this file
# so be it for now

DELAY_TIME = 60


@celery_app.task(base=DBTask, bind=True)
def migrate_data_files_from_fhir_to_sql(self):
    data_dir = os.path.join(settings.root_dir, settings.data_dir)
    for filename in os.listdir(data_dir):
        full_filename = os.path.join(data_dir, filename)
        date_last_modified = os.path.getmtime(full_filename)
        if not self.session.query(
            CeleryFHIRMigration.query.filter(
                CeleryFHIRMigration.file_name == filename,
                CeleryFHIRMigration.date_last_modified
                < (date_last_modified - DELAY_TIME),
            ).exists()
        ).scalar():
            # celery_worker_1  | LINE 3: ...son' AND celery_fhir_migration.date_last_modified < 16794825...
            # celery_worker_1  |                                                              ^
            # celery_worker_1  | HINT:  No operator matches the given name and argument types. You might need to add explicit type casts.
            # celery_worker_1  |
            # celery_worker_1  | [SQL: SELECT EXISTS (SELECT 1
            # celery_worker_1  | FROM celery_fhir_migration
            # celery_worker_1  | WHERE celery_fhir_migration.file_name = %(file_name_1)s AND celery_fhir_migration.date_last_modified < %(date_last_modified_1)s) AS anon_1]
            # celery_worker_1  | [parameters: {'file_name_1': 'Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json', 'date_last_modified_1': 1679482517.6400082}]
            # celery_worker_1  | (Background on this error at: https://sqlalche.me/e/20/f405)
            print("HERE")
            continue
        # Do something with the file
