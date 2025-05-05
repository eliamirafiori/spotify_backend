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
from ..crud.albums import (
    create_album,
    read_albums,
    read_album,
    read_album_songs,
    update_album,
    delete_album,
)
from ..models.album_model import AlbumCreate, AlbumPublic, AlbumUpdate
from ..models.song_model import SongPublic

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for albums
router = APIRouter(
    prefix="/albums",  # router prefix url
    tags=["albums"],  # router tag
)


@router.post(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=AlbumPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_album(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    album: Annotated[
        AlbumCreate, Form()
    ],  # request must pass a Form body with AlbumCreate fields
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Create a new album.
    Here you can insert album informations, then to upload its files you have to use the upload endpoint.

    \f

    :param session: SQLModel session
    :type session: Session
    :param album: Album Body that needs to be posted on DB
    :type album: AlbumCreate
    :return: The new created Album
    :rtype: AlbumPublic
    """
    # save the album data to db
    return await create_album(session=session, album=album)


@router.get(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[AlbumPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_albums(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    params: CommonQueryParams = Depends(),
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all albums with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of albums
    :rtype: list[AlbumPublic]
    """
    return await read_albums(session=session, params=params)


@router.get(
    "/{song_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=AlbumPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_album(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    album_id: Annotated[int, Path()],  # get path parameter
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get specific album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param album_id: Album's ID
    :type album_id: int
    :return: Album or None
    :rtype: AlbumPublic | None
    """
    return await read_album(session=session, id=album_id)


@router.get(
    "/{album_id}/songs",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[SongPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_album_songs(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    album_id: Annotated[int, Path()],
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all songs from album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param album_id: Album's ID
    :type album_id: int
    :return: List of songs
    :rtype: list[SongPublic]
    """
    return await read_album_songs(session=session, id=album_id)


@router.put(
    "/{album_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_UPDATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=AlbumPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def put_album(
    session: SessionDep,
    album_id: Annotated[int, Path()],
    album: Annotated[AlbumUpdate, Form()],
) -> Any:
    """
    Update specific album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param album_id: Album's ID
    :type album_id: int
    :param album: The album's data
    :type album: AlbumUpdate
    :return: Album instance
    :rtype: AlbumPublic
    """
    return await update_album(session=session, id=album_id, album=album)


@router.delete(
    "/{album_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_DELETE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=None,  # the model used to format the response
    status_code=204,  # HTTP status code returned if no errors occur
)
async def del_album(
    session: SessionDep,
    album_id: Annotated[int, Path()],
) -> Any:
    """
    Delete specific album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param album_id: Album's ID
    :type album_id: int
    :return: Nothing
    :rtype: None
    """
    return await delete_album(session=session, id=album_id)
