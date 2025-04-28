from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine


# SQLite database URL
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///./{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


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