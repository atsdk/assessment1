from __future__ import annotations

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.database import Model
from app.core import settings


@pytest.fixture(scope="session")
def engine():
    """Creates a test database and returns an engine.
    After the test it drops the database
    """
    url = f"{settings.database_uri}/testdb"
    db_engine = create_engine(url)
    if database_exists(url):
        drop_database(url)
    create_database(url)

    yield db_engine

    drop_database(url)


@pytest.fixture(scope="session")
def tables(engine):
    """Creates all tables in the database. After the test it drops all"""
    Model.metadata.create_all(engine)
    yield
    Model.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down
    everything properly.
    """
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
