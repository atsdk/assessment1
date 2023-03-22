from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core import settings


engine = create_engine(settings.database_uri)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


Model = declarative_base(name="Model")
Model.query = db_session.query_property()
