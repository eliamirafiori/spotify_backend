from typing import Annotated, Any
from uuid import UUID

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Security,
    Path,
    Body,
)
from sqlmodel import Session, select

from ..models.user_model import (
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)
from ..core.database import get_session
from ..core.auth_utils import get_current_active_user
from ..commons.enums import Scope
from ..commons.common_query_params import CommonQueryParams
from ..crud.users import create_user, read_user, read_users, update_user, delete_user

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    dependencies=[Security(get_current_active_user, scopes=[Scope.USERS_CREATE])],
    response_model=UserPublic,
    status_code=201,
)
async def post_user(
    session: SessionDep,
    user: Annotated[UserCreate, Body()],
) -> Any:
    """
    Create a new user.

    \f

    :param user: User to create
    :type user: UserCreate
    :param session: SQLModel session
    :type session: Session
    :return: Created user
    :rtype: UserPublic
    """
    return await create_user(session=session, user=user)


@router.get(
    "/",
    dependencies=[Security(get_current_active_user, scopes=[Scope.USERS_READ])],
    response_model=list[UserPublic],
    status_code=200,
)
async def get_users(
    session: SessionDep,
    params: CommonQueryParams = Depends(),
) -> Any:
    """
    Get all users with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of users
    :rtype: list[UserPublic]
    """
    return await read_users(session=session, params=params)


@router.get(
    "/{user_id}",
    dependencies=[Security(get_current_active_user, scopes=[Scope.USERS_READ])],
    response_model=UserPublic,
    status_code=200,
)
async def get_user(
    session: SessionDep,
    user_id: Annotated[UUID, Path()],
) -> Any:
    """
    Get specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param user_id: User's ID
    :type user_id: UUID
    :return: User or None
    :rtype: UserPublic | None
    """
    return await read_users(session=session, filter=user_id)


@router.put(
    "/{user_id}",
    dependencies=[Security(get_current_active_user, scopes=[Scope.USERS_UPDATE])],
    response_model=UserPublic,
    status_code=200,
)
async def put_user(
    session: SessionDep,
    user_id: Annotated[UUID, Path()],
    user: UserUpdate,
) -> Any:
    """
    Update specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: User's ID
    :type id: int
    :param user: The user's data
    :type user: UserCreate
    :return: User instance
    :rtype: UserPublic
    """
    return await update_user(session=session, id=user_id, user=user)


@router.delete(
    "/{user_id}",
    dependencies=[Security(get_current_active_user, scopes=[Scope.USERS_DELETE])],
    response_model=None,
    status_code=204,
)
async def del_user(
    session: SessionDep,
    user_id: Annotated[UUID, Path()],
) -> None:
    """
    Delete specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: User's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    await delete_user(session=session, id=user_id)