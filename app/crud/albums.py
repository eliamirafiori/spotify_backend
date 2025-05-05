from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, or_, select

from ..commons.common_query_params import CommonQueryParams
from ..models.album_model import Album, AlbumCreate, AlbumPublic, AlbumUpdate
from ..models.song_model import Song, SongPublic


async def create_album(
    session: Session,
    album: AlbumCreate,
) -> AlbumPublic:
    """
    Create a new album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param album: Album to create
    :type album: AlbumCreate
    :return: Created song
    :rtype: AlbumPublic
    """
    db_album = Album.model_validate(album)
    session.add(db_album)
    session.commit()
    session.refresh(db_album)
    return db_album


async def read_albums(
    session: Session,
    params: CommonQueryParams = Depends(),
) -> list[AlbumPublic]:
    """
    Get all albums with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of songs
    :rtype: list[AlbumPublic]
    """
    return session.exec(select(Album).offset(params.offset).limit(params.limit)).all()


async def read_album(
    session: Session,
    id: Annotated[int, Body()],
) -> AlbumPublic | None:
    """
    Get specific album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: String to filter on
    :type id: int
    :return: Album or None
    :rtype: AlbumPublic | None
    """

    return session.exec(select(Album).where(Album.id == id)).first()


async def read_album_songs(
    session: Session,
    id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Get album's songs.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Album's ID
    :type id: int
    :return: List of the album's songs
    :rtype: list[SongPublic]
    """
    # check if album exists
    db_album = session.get(Album, id)  # get the existing album instance
    if not db_album:  # check if the album exists
        raise HTTPException(status_code=404, detail="Album not found")

    return session.exec(select(Song).where(Song.album_id == id)).all()


async def update_album(
    session: Session,
    id: int,
    album: AlbumUpdate,
) -> AlbumPublic:
    """
    Update specific album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Album's ID
    :type id: int
    :param album: The album's data
    :type album: AlbumCreate
    :return: Album instance
    :rtype: AlbumPublic
    """
    db_album = session.get(Album, id)  # get the existing album instance
    if not db_album:  # check if the album exists
        raise HTTPException(status_code=404, detail="Album not found")

    album_data = album.model_dump(exclude_unset=True)  # get only updated values
    for key, value in album_data.items():  # iterate through album's data
        # map key and value from album's data to its db instance
        setattr(db_album, key, value)

    session.add(db_album)  # add the updated version to the DB
    session.commit()  # commit the cheanges to the DB
    session.refresh(db_album)  # refresh the db_song instance
    return db_album


async def delete_album(
    session: Session,
    id: int,
) -> None:
    """
    Delete specific album.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Album's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    db_album = session.get(Album, id)  # get the existing album instance
    if not db_album:  # check if the album exists
        raise HTTPException(status_code=404, detail="Album not found")

    session.delete(db_album)  # delete the instance of the album
    session.commit()  # commit the changes to the DB
