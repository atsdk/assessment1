from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from app.core import settings


engine = create_engine(settings.database_uri, pool_size=5, max_overflow=2)
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Model = declarative_base(name="Model")
