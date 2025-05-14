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
from ..crud.playlists import (
    create_playlist,
    read_playlists,
    read_playlist,
    update_playlist,
    delete_playlist,
    read_playlist_songs,
    create_playlist_song_link,
    delete_playlist_song_link,
)
from ..models.playlist_model import PlaylistCreate, PlaylistPublic, PlaylistUpdate
from ..models.song_model import SongPublic

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for playlists
router = APIRouter(
    prefix="/playlists",  # router prefix url
    tags=["playlists"],  # router tag
)


@router.post(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=PlaylistPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_playlist(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    playlist: Annotated[
        PlaylistCreate, Form()
    ],  # request must pass a Form body with PlaylistCreate fields
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Create a new playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist: Playlist Body that needs to be posted on DB
    :type playlist: PlaylistCreate
    :return: The new created Playlist
    :rtype: PlaylistPublic
    """
    # save the playlist data to db
    return await create_playlist(session=session, playlist=playlist)


@router.get(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[PlaylistPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_playlists(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    params: CommonQueryParams = Depends(),
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all playlists with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of playlists
    :rtype: list[PlaylistPublic]
    """
    return await read_playlists(session=session, params=params)


@router.get(
    "/{playlist_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=PlaylistPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_playlist(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    playlist_id: Annotated[int, Path()],  # get path parameter
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get specific playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :return: Playlist or None
    :rtype: PlaylistPublic | None
    """
    return await read_playlist(session=session, id=playlist_id)


@router.put(
    "/{playlist_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_UPDATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=PlaylistPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def put_playlist(
    session: SessionDep,
    playlist_id: Annotated[int, Path()],
    playlist: Annotated[PlaylistUpdate, Form()],
) -> Any:
    """
    Update specific playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :param playlist: The playlist's data
    :type playlist: PlaylistUpdate
    :return: Playlist instance
    :rtype: PlaylistPublic
    """
    return await update_playlist(session=session, id=playlist_id, playlist=playlist)


@router.delete(
    "/{playlist_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_DELETE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=None,  # the model used to format the response
    status_code=204,  # HTTP status code returned if no errors occur
)
async def del_playlist(
    session: SessionDep,
    playlist_id: Annotated[int, Path()],
) -> Any:
    """
    Delete specific playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :return: Nothing
    :rtype: None
    """
    return await delete_playlist(session=session, id=playlist_id)

# below there are all the link related operations

@router.get(
    "/{playlist_id}/songs",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[SongPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_playlist_song_link(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    playlist_id: Annotated[int, Path()],
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get playlist's songs.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Playlist's ID
    :type id: int
    :return: List of the playlist's songs
    :rtype: list[SongPublic]
    """
    # save the link to db
    return await read_playlist_songs(
        session=session,
        id=playlist_id,
    )


@router.post(
    "/{playlist_id}/{song_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[SongPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_playlist_song_link(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    playlist_id: Annotated[int, Path()],
    song_id: Annotated[int, Path()],
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Add specific song to a playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :param song_id: Song's ID
    :type song_id: int
    :return: List of songs contained in the playlist
    :rtype: list[SongPublic]
    """
    # save the link to db
    return await create_playlist_song_link(
        session=session,
        playlist_id=playlist_id,
        song_id=song_id,
    )


@router.delete(
    "/{playlist_id}/{song_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_DELETE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=None,  # the model used to format the response
    status_code=204,  # HTTP status code returned if no errors occur
)
async def del_playlist_song_link(
    session: SessionDep,
    playlist_id: Annotated[int, Path()],
    song_id: Annotated[int, Path()],
) -> Any:
    """
    Delete specific song from a playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :param song_id: Song's ID
    :type song_id: int
    :return: Nothing
    :rtype: None
    """
    # delete the link from db
    return await delete_playlist_song_link(
        session=session,
        playlist_id=playlist_id,
        song_id=song_id,
    )
