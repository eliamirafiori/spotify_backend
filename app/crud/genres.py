from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, select

from ..commons.common_query_params import CommonQueryParams
from ..models.genre_model import Genre, GenreCreate, GenrePublic, GenreUpdate
from ..models.song_model import Song, SongPublic
from ..models.relationship_song_genre import SongGenreLink


async def create_genre(
    session: Session,
    genre: GenreCreate,
) -> GenrePublic:
    """
    Create a new genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param genre: Genre to create
    :type genre: GenreCreate
    :return: Created song
    :rtype: GenrePublic
    """
    db_genre = Genre.model_validate(genre)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


async def read_genres(
    session: Session,
    params: CommonQueryParams = Depends(),
) -> list[GenrePublic]:
    """
    Get all genres with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of songs
    :rtype: list[GenrePublic]
    """
    return session.exec(select(Genre).offset(params.offset).limit(params.limit)).all()


async def read_genre(
    session: Session,
    id: Annotated[int, Body()],
) -> GenrePublic | None:
    """
    Get specific genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: String to filter on
    :type id: int
    :return: Genre or None
    :rtype: GenrePublic | None
    """

    return session.exec(select(Genre).where(Genre.id == id)).first()


async def create_genre_song(
    session: Session,
    genre_id: Annotated[int, Body()],
    song_id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Add a song to a genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param genre_id: Genre's ID
    :type genre_id: int
    :param song_id: Song's ID
    :type song_id: int
    :return: List of the genre's songs
    :rtype: list[SongPublic]
    """
    # check if genre exists
    db_genre = session.get(Genre, id)  # get the existing genre instance
    if not db_genre:  # check if the genre exists
        raise HTTPException(status_code=404, detail="Genre not found")

    # check if song exists
    db_song = session.get(Song, id)  # get the existing song instance
    if not db_song:  # check if the song exists
        raise HTTPException(status_code=404, detail="Song not found")

    # check if link exists
    db_link = session.exec(
        select(SongGenreLink).where(
            SongGenreLink.genre_id == genre_id,
            SongGenreLink.song_id == song_id,
        )
    ).fist()  # get the existing link instance
    if db_link:  # check if the link exists
        raise HTTPException(
            status_code=404, detail="Relationship between Song and Genre found"
        )

    data_link: SongGenreLink = SongGenreLink(genre_id=genre_id, song_id=song_id)
    session.add(data_link)
    session.commit()

    return read_genre_songs(session=session, id=genre_id)


async def read_genre_songs(
    session: Session,
    id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Get genre's songs.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Genre's ID
    :type id: int
    :return: List of the genre's songs
    :rtype: list[SongPublic]
    """
    # check if genre exists
    db_genre = session.get(Genre, id)  # get the existing genre instance
    if not db_genre:  # check if the genre exists
        raise HTTPException(status_code=404, detail="Genre not found")

    # The condition "SongPlaylistLink.song_id == Song.id" in the "where" clause is unnecessary,
    # because the join method already establishes the relationship between "Song" and "SongGenreLink"
    # based on the foreign key. Including this condition can lead to confusion and potential errors.
    # return session.exec(
    #     select(Song).join(SongGenreLink).where(SongGenreLink.genre_id == id)
    # ).all()
    return session.exec(select(Song).join(SongGenreLink)).all()


async def update_genre(
    session: Session,
    id: int,
    genre: GenreUpdate,
) -> GenrePublic:
    """
    Update specific genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Genre's ID
    :type id: int
    :param genre: The genre's data
    :type genre: GenreCreate
    :return: Genre instance
    :rtype: GenrePublic
    """
    db_genre = session.get(Genre, id)  # get the existing genre instance
    if not db_genre:  # check if the genre exists
        raise HTTPException(status_code=404, detail="Genre not found")

    genre_data = genre.model_dump(exclude_unset=True)  # get only updated values
    for key, value in genre_data.items():  # iterate through genre's data
        # map key and value from genre's data to its db instance
        setattr(db_genre, key, value)

    session.add(db_genre)  # add the updated version to the DB
    session.commit()  # commit the cheanges to the DB
    session.refresh(db_genre)  # refresh the db_song instance
    return db_genre


async def delete_genre(
    session: Session,
    id: int,
) -> None:
    """
    Delete specific genre.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Genre's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    db_genre = session.get(Genre, id)  # get the existing genre instance
    if not db_genre:  # check if the genre exists
        raise HTTPException(status_code=404, detail="Genre not found")

    session.delete(db_genre)  # delete the instance of the genre
    session.commit()  # commit the changes to the DB
