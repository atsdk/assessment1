# EMIS Group test task
done by Oleksii Svintsitskyi

The main idea of the application is to save files to the files system
using

/api/v1/patient-data endpoint (doc: http://127.0.0.1:8000/redoc)

Endpoint saves the file to the data directory (specified in api.core.settings)
and sends data migration task to Celery via RabbitMQ.
Then concurrent Celery worker parses the FHIR file and saves to Postgres.

An alternate (actually, preferable) solution would be to
migrate data once in a while (let's say, once an hour) with a
background task scheduler.

Relational model itself consists of two examples:

PatientAllergyIntolerance + Allergy tables - example of relations

Other tables - example of using JSONB

So, as appliation would evolve we would see more and more fields moving
out of JSONB to separate fields.