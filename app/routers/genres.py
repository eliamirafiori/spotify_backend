from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Form,
    Depends,
    Path,
    Security,
)
from sqlmodel import Session

from ..commons.common_query_params import CommonQueryParams
from ..commons.enums import Scope
from ..core.auth_utils import get_current_active_user
from ..core.database import get_session
from ..crud.genre import (
    create_genre,
    read_genres,
    read_genre,
    update_genre,
    delete_genre,
)
from ..models.genre_model import GenreCreate, GenrePublic, GenreUpdate

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for genres
router = APIRouter(
    prefix="/genres",  # router prefix url
    tags=["genres"],  # router tag
)


@router.post(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=GenrePublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_genre(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    genre: Annotated[
        GenreCreate, Form()
    ],  # request must pass a Form body with GenreCreate fields
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Create a new genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param genre: Genre Body that needs to be posted on DB
    :type genre: GenreCreate
    :return: The new created Genre
    :rtype: GenrePublic
    """
    # save the genre data to db
    return await create_genre(session=session, genre=genre)


@router.get(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[GenrePublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_genres(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    params: CommonQueryParams = Depends(),
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all genres with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of genres
    :rtype: list[GenrePublic]
    """
    return await read_genres(session=session, params=params)


@router.get(
    "/{genre_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=GenrePublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_genre(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    genre_id: Annotated[int, Path()],  # get path parameter
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get specific genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param genre_id: Genre's ID
    :type genre_id: int
    :return: Genre or None
    :rtype: GenrePublic | None
    """
    return await read_genre(session=session, id=genre_id)


@router.put(
    "/{genre_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_UPDATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=GenrePublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def put_genre(
    session: SessionDep,
    genre_id: Annotated[int, Path()],
    genre: Annotated[GenreUpdate, Form()],
) -> Any:
    """
    Update specific genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param genre_id: Genre's ID
    :type genre_id: int
    :param genre: The genre's data
    :type genre: GenreUpdate
    :return: Genre instance
    :rtype: GenrePublic
    """
    return await update_genre(session=session, id=genre_id, genre=genre)


@router.delete(
    "/{genre_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_DELETE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=None,  # the model used to format the response
    status_code=204,  # HTTP status code returned if no errors occur
)
async def del_genre(
    session: SessionDep,
    genre_id: Annotated[int, Path()],
) -> Any:
    """
    Delete specific genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param genre_id: Genre's ID
    :type genre_id: int
    :return: Nothing
    :rtype: None
    """
    return await delete_genre(session=session, id=genre_id)
