# EMIS Group test task
### done by Oleksii Svintsitskyi

The main idea of the application is to save files to the file system using

**/api/v1/patient-data** endpoint (see doc: http://127.0.0.1:8000/redoc)

Endpoint saves the file to the **data** directory (specified in **api.core.settings**)
and sends data migration task to Celery via RabbitMQ.
Then, concurrent Celery worker parses the FHIR file and saves to Postgres.

An alternate (actually, preferable) solution would be to
migrate data once in a while (let's say, once an hour) with a
background task scheduler. But that would be not so convenient to present.

### Relational model itself consists of two examples:

**PatientAllergyIntolerance** + **Allergy tables** - example of **relationship**

**Other tables** - example of using **JSONB**

As appliation would evolve we would see more and more fields moving
out of JSONB to separate fields.

## How to run

`docker-compose up -d`

## How to test

`python3 upload_all_files.py --folder /path/to/folder/with/data_files.json`

### Other notes

Sometimes, right after the start of the database, **pcycopg2** will raise some excptions because of random problems with the session.
If that happens, you can just wait until upload_all_files finished the job and start it again, it won't happen again. But I had no time to find out the root cause.
To check maximum speeed of data migration, run TRUNCATE ALL sql query to make tables empty.
Also, you can check some other queries I've provided.
