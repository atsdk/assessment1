from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core import settings


engine = create_engine(settings.database_uri, pool_size=5, max_overflow=2)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Model = declarative_base(name="Model")
