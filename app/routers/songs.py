import os
import aiofiles
import json

from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Form,
    Depends,
    HTTPException,
    Path,
    Security,
    File,
    UploadFile,
)
from pydantic import ValidationError
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
        str, Form()
    ],  # request must pass a Form body with SongCreate fields
    file: Annotated[UploadFile, File()],  # the song in a file-like object
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
    print("STEP 1")
    try:
        song_dict = json.loads(song)
        song = SongCreate(**song_dict)
        print(f"SONG: {song}")
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=400, detail="Invalid song data") from e
    
    # save the song data to db
    db_song = await create_song(session=session, song=song)

    print("STEP 2")
    # we get its path
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # get the directory of this file

    file_extension = file.content_type.split("/")[1]

    song_path = os.path.join(
        base_dir, "..", f"public/audio/{db_song.id}.{file_extension}"
    )  # Construct the absolute path

    print("STEP 3")
    # we save the path to the song_url field
    updated_song: SongUpdate = db_song
    updated_song.song_url = song_path

    print("STEP 4")
    # we save the song on disk
    async with aiofiles.open(song_path, "wb") as out_file:
        # the whole song is saved in memory first
        content = await file.read()  # async read
        await out_file.write(content)  # async write

        # alternative way, save in chunks
        # this way is better for videos or large files
        # while content := await file.read(1024):  # async read chunk
        #     await out_file.write(content)  # async write chunk

    print("STEP 5")
    return await update_song(session=session, id=db_song.id, song=updated_song)


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
    song_id: Annotated[int, Path()],  # get path parameter
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Get specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song_id: Song's ID
    :type song_id: int
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
    song_id: Annotated[int, Path()],
    song: SongUpdate,
) -> Any:
    """
    Update specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song_id: Song's ID
    :type song_id: int
    :param song: The song's data
    :type song: SongCreate
    :return: Song instance
    :rtype: SongPublic
    """
    return await update_song(session=session, id=song_id, song=song)


# TODO: DELETE
