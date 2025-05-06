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
from ..crud.artists import (
    create_artist,
    read_artists,
    read_artist,
    read_artist_songs,
    update_artist,
    delete_artist,
)
from ..models.artist_model import ArtistCreate, ArtistPublic, ArtistUpdate
from ..models.song_model import SongPublic

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for artists
router = APIRouter(
    prefix="/artists",  # router prefix url
    tags=["artists"],  # router tag
)


@router.post(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=ArtistPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_artist(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    artist: Annotated[
        ArtistCreate, Form()
    ],  # request must pass a Form body with ArtistCreate fields
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Create a new artist.
    Here you can insert artist informations, then to upload its files you have to use the upload endpoint.

    \f

    :param session: SQLModel session
    :type session: Session
    :param artist: Artist Body that needs to be posted on DB
    :type artist: ArtistCreate
    :return: The new created Artist
    :rtype: ArtistPublic
    """
    # save the artist data to db
    return await create_artist(session=session, artist=artist)


@router.get(
    "/",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[ArtistPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_artists(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    params: CommonQueryParams = Depends(),
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all artists with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of artists
    :rtype: list[ArtistPublic]
    """
    return await read_artists(session=session, params=params)


@router.get(
    "/{artist_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=ArtistPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_artist(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    artist_id: Annotated[int, Path()],  # get path parameter
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get specific artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param artist_id: Artist's ID
    :type artist_id: int
    :return: Artist or None
    :rtype: ArtistPublic | None
    """
    return await read_artist(session=session, id=artist_id)


@router.get(
    "/{artist_id}/songs",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_READ])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=list[SongPublic],  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def get_artist_songs(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    artist_id: Annotated[int, Path()],
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get all songs from artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param artist_id: Artist's ID
    :type artist_id: int
    :return: List of songs
    :rtype: list[SongPublic]
    """
    return await read_artist_songs(session=session, id=artist_id)


@router.put(
    "/{artist_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_UPDATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=ArtistPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def put_artist(
    session: SessionDep,
    artist_id: Annotated[int, Path()],
    artist: Annotated[ArtistUpdate, Form()],
) -> Any:
    """
    Update specific artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param artist_id: Artist's ID
    :type artist_id: int
    :param artist: The artist's data
    :type artist: ArtistUpdate
    :return: Artist instance
    :rtype: ArtistPublic
    """
    return await update_artist(session=session, id=artist_id, artist=artist)


@router.delete(
    "/{artist_id}",
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_DELETE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=None,  # the model used to format the response
    status_code=204,  # HTTP status code returned if no errors occur
)
async def del_artist(
    session: SessionDep,
    artist_id: Annotated[int, Path()],
) -> Any:
    """
    Delete specific artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param artist_id: Artist's ID
    :type artist_id: int
    :return: Nothing
    :rtype: None
    """
    return await delete_artist(session=session, id=artist_id)
