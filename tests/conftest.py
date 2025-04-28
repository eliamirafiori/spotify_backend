import pytest

from contextlib import contextmanager

from fastapi.testclient import TestClient

from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from ..main import app
from ..core.database import get_session, get_session_directly


# SQLite database URL
sqlite_url = f"sqlite://" # Creates a temporary database in RAM

# Create an in-memory SQLite database engine
connect_args = {"check_same_thread": False}
engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
    poolclass=StaticPool,  # This pool class ensures that the same connection is used throughout the session, which is necessary for in-memory databases.
)


@pytest.fixture(scope="session")
def get_token() -> str:
    # Token to access limited endpoints
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb3JlbWlwc3VtIiwic2NvcGVzIjpbXX0.pMoQKRXc3_r5Bgk3iSxed_6Uzh2-Sns6C5oKyUqtsSs"


@pytest.fixture(scope="session")
def db_engine():
    # Create all tables before the test session
    SQLModel.metadata.create_all(engine)
    yield engine
    # Drop all tables after the test session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Creates a new database session for a test.
    """
    # Create a new session for a test
    with Session(db_engine) as session:
        yield session
        # Rollback any changes made during the test
        # session.rollback()


@pytest.fixture(scope="function")
@contextmanager
def db_session_directly(db_engine):
    """
    Creates a new database session direcly for a test.
    """
    # Create a new session for a test
    with Session(db_engine) as session:
        yield session
        # Rollback any changes made during the test
        # session.rollback()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Creates a new FastAPI TestClient that uses the test database session.
    """

    # Override the get_session dependency to use the test database session
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    # Override the get_session_directly dependency to use the test database session
    def override_get_session_directly():
        yield db_session_directly

    app.dependency_overrides[get_session_directly] = override_get_session_directly

    with TestClient(app) as c:
        yield c

    # Clear overrides after the test to prevent side effects
    app.dependency_overrides.clear()