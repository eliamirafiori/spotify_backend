import os

from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Security,
)
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, select

from ..commons.constants import AUDIO_DIRECTORY
from ..commons.enums import Scope
from ..core.auth_utils import get_current_active_user
from ..core.database import get_session

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for downloads
router = APIRouter(
    prefix="/downloads",  # router prefix url
    tags=["downloads"],  # router tag
)


@router.get(
    "/audio/{song_id}",  # endpoint url after the prefix specified earlier
    dependencies=[
        Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])
    ],  # security check, user needs to have permissions to interact with this endpoint
    response_model=None,  # the model used to format the response
    status_code=201,  # HTTP status code returned if no errors occur
)
async def download_audio(
    session: SessionDep,  # request must pass a JWT, with this dependency we extract its data to verify the user
    song_id: Annotated[int, Path()],  # the song ID
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
    # TODO: get file extension from db

    file_path = os.path.join(AUDIO_DIRECTORY, f"{song_id}.mp3")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # for small files this load the whole file in memory
    return FileResponse(
        path=file_path,
        filename=f"song_{song_id}",
        media_type="application/octet-stream",
    )

    # for large files its better to stream the file in chunks
    # def iterfile():
    #     with open(file_path, mode="rb") as file_like:
    #         yield from file_like
    #
    # headers = {
    #     "Content-Disposition": f'attachment; filename="mamma_{song_id}"'
    # }
    #
    # return StreamingResponse(iterfile(), headers=headers, media_type="application/octet-stream")
