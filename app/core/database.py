from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

from ..commons.constants import (
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_SERVER,
    POSTGRES_USER,
)


# SQLite database URL
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///./{sqlite_file_name}"

# PostgreSQl database URL
# needs Python package: pip install "psycopg[binary]"
postgresql_url = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

connect_args = {"check_same_thread": False}
engine = create_engine(postgresql_url)


def init_db():
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Yields a session, usefull for dependencies in a route.
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_directly():
    """
    Yields a session direcly, usefull for calling directly functions not for handling a request to a route.
    """
    with Session(engine) as session:
        yield session
