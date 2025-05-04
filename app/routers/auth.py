from datetime import timedelta
from typing import Annotated, Any

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..models.user_model import (
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)
from ..models.token_model import Token
from ..core.database import get_session
from ..core.auth_utils import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from ..crud.users import read_user, check_username

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

"""
@router.post("/refresh")
def refresh_token(request: Request,
    session: SessionDep,):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        # Verify token is in database and not expired or revoked
        # If valid, issue new tokens
        access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})
        # Store new_refresh_token in database and invalidate the old one
        response = JSONResponse(content={"access_token": access_token})
        response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
"""


@router.post("/signin", response_model=Token, status_code=200)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = await authenticate_user(
        form_data.username,
        form_data.password,
        session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": user.username,  # Or user's ID
            "scopes": form_data.scopes,  # TODO: fetch which scopes the user has access to
        },
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", response_model=UserPublic, status_code=201)
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Any:
    user: UserCreate = UserCreate
    user.username = form_data.username
    user.hashed_password = get_password_hash(form_data.password)

    if not user.username or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Username or password not spcified")

    db_user = await check_username(session=session, filter=user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already taken")

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user