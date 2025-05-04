from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from sqlmodel import Session, select, or_
from passlib.context import CryptContext
from pydantic import ValidationError

from ..commons.enums import Scope
from ..models.user_model import (
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)
from ..models.token_model import Token, TokenData
from .database import get_session, get_session_directly

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "357e8ab8af47bbcf66962ce2841dbe522d4f9e4a001bdb19101561467fdae00b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

SessionDep = Annotated[Session, Depends(get_session)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/signin",  # Must be the same PATH of the endpoint
    scopes={scope.value: f"Access to {scope.value}" for scope in Scope}
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the given password matches the hashed one.

    /f

    :param plain_password: The given password
    :type plain_password: str
    :param hashed_password: The hashed password from the database
    :type hashed_password: str
    :return: If the two password matches
    :rtype: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes the given password.

    /f

    :param password: The given password
    :type password: str
    :return: The hashed password
    :rtype: str
    """
    return pwd_context.hash(password)


async def get_user(username: str, session: SessionDep) -> User | None:
    """
    Retrieves the user associated to this username from the database.

    ​In FastAPI, when you need to perform database queries outside of route handlers,
    such as within utility functions or services, you should manage the database session explicitly.

    This approach ensures that your functions remain decoupled from
    FastAPI's dependency injection system, promoting better modularity and testability.

    /f

    :param username: The given username
    :type username: str
    :param session: The database session dependency
    :type session: SessionDep
    :return: The User from the database or None if not found
    :rtype: User | None
    """
    user = session.exec(
        select(User).where(
            or_(
                User.username == username,
                User.email == username,
            )
        ),
    ).first()

    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: SecurityScopes,
) -> UserPublic:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(f"USERNAME: {username}")

        if username is None:
            raise credentials_exception

        # Verifying the expiration date is unnecessary.
        # Because PyJWT is such a great tool,
        # it already took care of handling the verification for you,
        # so if you try to decode an expired token,
        # you should see an error like this: ExpiredSignatureError
        # expiration = payload.get("exp")
        # if datetime.now(timezone.utc) > datetime.fromtimestamp(expiration, tz=timezone.utc):
        #     raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (InvalidTokenError, ValidationError):
        print(f"ERROR 1:")
        raise credentials_exception

    with get_session_directly() as session:
        user = await get_user(username=token_data.username, session=session)
        print(f"USER: {user}")
        if user is None:
            print(f"ERROR 2: {user}")
            raise credentials_exception

        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user


async def get_current_active_user(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
) -> UserPublic:
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(
    username: str,
    password: str,
    session: SessionDep,
) -> UserPublic:
    """
    Check and eventually retrieves the user associated to this username from the database.
    Then checks if the given password matches the one in the database.
    Before returning the User, it implicit cast it to UserPublic to remove the hashed_password variable.

    /f

    :param username: The given username
    :type username: str
    :param password: The given password
    :type password: str
    :return: The UserPublic from the database
    :rtype: UserPublic
    """
    user = await get_user(username, session)
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    """
    Create the JWT encoding the 'sub' and the 'exp' keys.
    Usually the 'sub' contains the user identification.

    /f

    :param data: The content to be encoded into the JWT
    :type data: dict
    :param expires_delta: The expiration time delta
    :type expires_delta: timedelta | None = timedelta(minutes=10)
    :return: The JWT
    :rtype: str
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict,
    expires_delta: timedelta | None = timedelta(days=7),
) -> str:
    """
    Create the JWT encoding the 'sub' and the 'exp' keys.
    Usually the 'sub' contains the user identification.

    /f

    :param data: The content to be encoded into the JWT
    :type data: dict
    :param expires_delta: The expiration time delta
    :type expires_delta: timedelta | None = timedelta(days=7)
    :return: The JWT
    :rtype: str
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt