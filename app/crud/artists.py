from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, select

from ..commons.common_query_params import CommonQueryParams
from ..models.artist_model import Artist, ArtistCreate, ArtistPublic, ArtistUpdate
from ..models.song_model import Song, SongPublic
from ..models.relationship_song_artist import SongArtistLink


async def create_artist(
    session: Session,
    artist: ArtistCreate,
) -> ArtistPublic:
    """
    Create a new artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param artist: Artist to create
    :type artist: ArtistCreate
    :return: Created song
    :rtype: ArtistPublic
    """
    db_artist = Artist.model_validate(artist)
    session.add(db_artist)
    session.commit()
    session.refresh(db_artist)
    return db_artist


async def read_artists(
    session: Session,
    params: CommonQueryParams = Depends(),
) -> list[ArtistPublic]:
    """
    Get all artists with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of songs
    :rtype: list[ArtistPublic]
    """
    return session.exec(select(Artist).offset(params.offset).limit(params.limit)).all()


async def read_artist(
    session: Session,
    id: Annotated[int, Body()],
) -> ArtistPublic | None:
    """
    Get specific artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: String to filter on
    :type id: int
    :return: Artist or None
    :rtype: ArtistPublic | None
    """

    return session.exec(select(Artist).where(Artist.id == id)).first()


async def read_artist_songs(
    session: Session,
    id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Get artist's songs.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Artist's ID
    :type id: int
    :return: List of the artist's songs
    :rtype: list[SongPublic]
    """
    # check if artist exists
    db_artist = session.get(Artist, id)  # get the existing artist instance
    if not db_artist:  # check if the artist exists
        raise HTTPException(status_code=404, detail="Artist not found")

    return session.exec(
        select(Song).join(SongArtistLink).where(SongArtistLink.artist_id == id)
    ).all()


async def update_artist(
    session: Session,
    id: int,
    artist: ArtistUpdate,
) -> ArtistPublic:
    """
    Update specific artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Artist's ID
    :type id: int
    :param artist: The artist's data
    :type artist: ArtistCreate
    :return: Artist instance
    :rtype: ArtistPublic
    """
    db_artist = session.get(Artist, id)  # get the existing artist instance
    if not db_artist:  # check if the artist exists
        raise HTTPException(status_code=404, detail="Artist not found")

    artist_data = artist.model_dump(exclude_unset=True)  # get only updated values
    for key, value in artist_data.items():  # iterate through artist's data
        # map key and value from artist's data to its db instance
        setattr(db_artist, key, value)

    session.add(db_artist)  # add the updated version to the DB
    session.commit()  # commit the cheanges to the DB
    session.refresh(db_artist)  # refresh the db_song instance
    return db_artist


async def delete_artist(
    session: Session,
    id: int,
) -> None:
    """
    Delete specific artist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Artist's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    db_artist = session.get(Artist, id)  # get the existing artist instance
    if not db_artist:  # check if the artist exists
        raise HTTPException(status_code=404, detail="Artist not found")

    session.delete(db_artist)  # delete the instance of the artist
    session.commit()  # commit the changes to the DB
