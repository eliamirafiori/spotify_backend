from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, or_, select

from ..commons.common_query_params import CommonQueryParams
from ..models.song_model import Song, SongCreate, SongPublic, SongUpdate


async def create_song(
    session: Session,
    song: SongCreate,
) -> SongPublic:
    """
    Create a new song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param song: Song to create
    :type song: SongCreate
    :return: Created song
    :rtype: SongPublic
    """
    db_song = Song.model_validate(song)
    session.add(db_song)
    session.commit()
    session.refresh(db_song)
    return db_song


async def read_songs(
    session: Session,
    params: CommonQueryParams = Depends(),
) -> list[SongPublic]:
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
    songs = session.exec(select(Song).offset(params.offset).limit(params.limit)).all()
    return songs


async def read_song(
    session: Session,
    id: Annotated[int, Body()],
) -> SongPublic | None:
    """
    Get specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: String to filter on
    :type id: int
    :return: Song or None
    :rtype: SongPublic | None
    """

    db_song = session.exec(select(Song).where(Song.id == id)).first()
    return db_song


async def update_song(
    session: Session,
    id: int,
    song: SongUpdate,
) -> SongPublic:
    """
    Update specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Song's ID
    :type id: int
    :param song: The song's data
    :type song: SongCreate
    :return: Song instance
    :rtype: SongPublic
    """
    db_song = session.get(Song, id)  # get the existing song instance
    if not db_song:  # check if the song exists
        raise HTTPException(status_code=404, detail="Song not found")

    song_data = song.model_dump(exclude_unset=True)  # get only updated values
    for key, value in song_data.items():  # iterate through song's data
        # map key and value from user's data to its db instance
        setattr(db_song, key, value)

    session.add(db_song)  # add the updated version to the DB
    session.commit()  # commit the cheanges to the DB
    session.refresh(db_song)  # refresh the db_song instance
    return db_song


async def delete_song(
    session: Session,
    id: int,
) -> None:
    """
    Delete specific song.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Song's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    db_song = session.get(Song, id)  # get the existing song instance
    if not db_song:  # check if the song exists
        raise HTTPException(status_code=404, detail="Song not found")

    session.delete(db_song)  # delete the instance of the song
    session.commit()  # commit the changes to the DB
