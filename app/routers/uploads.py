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
from ..core.file_utils import validate_audio_file
from ..core.database import get_session
from ..crud.songs import read_song, update_song
from ..models.song_model import Song, SongCreate, SongPublic, SongUpdate

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for uploads
router = APIRouter(
    prefix="/uploads",  # router prefix url
    tags=["uploads"],  # router tag
)


@router.post(
    "/songs/{song_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=SongPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_song(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    song_id: Annotated[int, Path()],  # the song ID
    file: Annotated[UploadFile, File()],  # the song in a file-like object
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Upload a new song file.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song_id: Song's ID
    :type song_id: int
    :param file: Song file
    :type file: UploadFile
    :return: The new created Song
    :rtype: SongPublic
    """
    # validate file
    validate_audio_file(file)

    # check if song record exists in db
    db_song: SongPublic = await read_song(session=session, id=song_id)
    if not db_song:
        raise HTTPException(4047, detail="Song not found")

    # we get current path
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # get the directory of this file

    file_extension = file.filename.split(".")[1]

    song_path = os.path.join(
        base_dir, "..", "..", f"public/audio/{song_id}.{file_extension}"
    )  # Construct the absolute path

    # we save the song on disk
    async with aiofiles.open(song_path, "wb") as out_file:
        # the whole song is saved in memory first
        content = await file.read()  # async read
        await out_file.write(content)  # async write

        # alternative way, save in chunks
        # this way is better for videos or large files
        # TODO: check wha tipy of file in args should be (maybe UploadFile is good, I dunno)
        # while content := await file.read(1024):  # async read chunk
        #     await out_file.write(content)  # async write chunk

    # we save the path to the song_url field
    # db_song: SongPublic = await read_song(session=session, id=song_id)
    db_song.song_url = song_path

    return await update_song(session=session, id=song_id, song=db_song)


@router.post(
    "/images/{song_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=SongPublic,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def post_song(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    song_id: Annotated[int, Path()],  # the song ID
    file: Annotated[UploadFile, File()],  # the song in a file-like object
) -> Any:  # returns Any because it gets overrided by the response_model
    """
    Upload a new song file.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song_id: Song's ID
    :type song_id: int
    :param file: Song file
    :type file: UploadFile
    :return: The new created Song
    :rtype: SongPublic
    """
    # we get current path
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # get the directory of this file

    file_extension = file.filename.split(".")[1]

    song_path = os.path.join(
        base_dir, "..", "..", f"public/audio/{song_id}.{file_extension}"
    )  # Construct the absolute path

    # we save the song on disk
    async with aiofiles.open(song_path, "wb") as out_file:
        # the whole song is saved in memory first
        content = await file.read()  # async read
        await out_file.write(content)  # async write

        # alternative way, save in chunks
        # this way is better for videos or large files
        # while content := await file.read(1024):  # async read chunk
        #     await out_file.write(content)  # async write chunk

    # we save the path to the song_url field
    db_song: SongPublic = await read_song(session=session, id=song_id)
    db_song.song_url = song_path

    return await update_song(session=session, id=song_id, song=db_song)
