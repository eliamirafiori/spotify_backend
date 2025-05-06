from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, or_, select

from ..commons.common_query_params import CommonQueryParams
from ..models.genre_model import Genre, GenreCreate, GenrePublic, GenreUpdate


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
