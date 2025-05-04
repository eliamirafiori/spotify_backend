from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, or_, select

from ..commons.common_query_params import CommonQueryParams
from ..models.user_model import User, UserCreate, UserPublic, UserUpdate


async def create_user(
    user: UserCreate,
    session: Session,
) -> UserPublic:
    """
    Create a new user.

    \f

    :param user: User to create
    :type user: UserCreate
    :param session: SQLModel session
    :type session: Session
    :return: Created user
    :rtype: UserPublic
    """
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


async def read_users(
    session: Session,
    params: CommonQueryParams = Depends(),
) -> list[UserPublic]:
    """
    Get all users with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of users
    :rtype: list[UserPublic]
    """
    users = session.exec(select(User).offset(params.offset).limit(params.limit)).all()
    return users


async def read_user(
    session: Session,
    id: int,
) -> UserPublic | None:
    """
    Get specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: User's ID
    :type id: int
    :return: User or None
    :rtype: UserPublic | None
    """

    db_user = session.exec(select(User).where(User.id == id)).first()
    if not db_user:
        raise HTTPException(404, detail="User not found")

    return db_user


async def check_username(
    session: Session,
    filter: str,
) -> UserPublic | None:
    """
    Get specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param filter: String to filter on
    :type filter: str
    :return: User or None
    :rtype: UserPublic | None
    """

    db_user = session.exec(
        select(User).where(
            or_(
                # User.id == filter,
                User.username == filter,
                User.email == filter,
            )
        )
    ).first()
    return db_user


async def update_user(
    session: Session,
    id: int,
    user: UserUpdate,
) -> UserPublic:
    """
    Update specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: User's ID
    :type id: int
    :param user: The user's data
    :type user: UserCreate
    :return: User instance
    :rtype: UserPublic
    """
    db_user = session.get(User, id)  # get the existing user instance
    if not db_user:  # check if the user exists
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)  # get only updated values
    for key, value in user_data.items():  # iterate through user's data
        # map key and value from user's data to its db instance
        setattr(db_user, key, value)

    session.add(db_user)  # add the updated version to the DB
    session.commit()  # commit the cheanges to the DB
    session.refresh(db_user)  # refresh the db_user instance
    return db_user


async def delete_user(
    session: Session,
    id: int,
) -> None:
    """
    Delete specific user.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: User's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    db_user = session.get(User, id)  # get the existing user instance
    if not db_user:  # check if the user exists
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(db_user)  # delete the instance of the user
    session.commit()  # commit the changes to the DB
