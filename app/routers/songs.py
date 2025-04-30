from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Security
from sqlmodel import Session, select

from ..commons.common_query_params import CommonQueryParams
from ..commons.enums import Scope
from ..core.auth_utils import get_current_active_user
from ..core.database import get_session
from ..crud.songs import create_song, delete_song, read_song, read_songs, update_song
from ..models.song_model import Song, SongCreate, SongPublic, SongUpdate

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for songs
router = APIRouter(
    prefix="/songs",  # router prefix url
    tags=["songs"],  # router tag
)


@router.post(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=SongPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_song(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    song: Annotated[
        SongCreate, Body()
    ],  # request must pass a Body with SongCreate fields
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Create a new song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song: Song Body that needs to be posted on DB
    :type song: SongCreate
    :return: The new created Song
    :rtype: SongPublic
    """
    return await create_song(session=session, song=song)


@router.get(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[SongPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_songs(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    params: CommonQueryParams = Depends(),
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all songs with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of songs
    :rtype: list[SongPublic]
    """
    return await read_songs(session=session, params=params)


@router.get(
    "/{song_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=SongPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_song(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    song_id: Annotated[UUID, Path()],  # get path parameter
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song_id: Song's ID
    :type song_id: UUID
    :return: User or None
    :rtype: SongPublic | None
    """
    return await read_song(session=session, id=song_id)


@router.put(
    "/{song_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=SongPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def put_song(
    session: SessionDep,
    song_id: Annotated[UUID, Path()],
    song: SongUpdate,
) -> Any:
    """
    Update specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song_id: Song's ID
    :type song_id: UUID
    :param song: The song's data
    :type song: SongCreate
    :return: Song instance
    :rtype: SongPublic
    """
    return await update_song(session=session, id=song_id, song=song)


# TODO: PUT
# TODO: DELETE
