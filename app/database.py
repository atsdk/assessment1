from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


engine = create_engine(settings.database_uri)


def get_session() -> Session:
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


db_session = get_session()

Model = declarative_base(name="Model")
Model.query = db_session.query_property()
