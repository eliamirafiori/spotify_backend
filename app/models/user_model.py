from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """
    Base model for User. This model is used to define the common fields.

    \f

    :param username: Username of the user
    :type username: str
    :param email: Email of the user
    :type email: str
    :param name: Name of the user
    :type name: str | None
    :param surname: Surname of the user
    :type surname: str | None
    :param image_url: User's profile image url
    :type image_url: str | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    username: str
    email: str
    name: str | None = None
    surname: str | None = None
    image_url: str | None = None
    is_disabled: bool | None = None

    model_config = {
        # "extra": "forbid",  # Otherwise is "allow"
        "json_schema_extra": {
            "examples": [
                {
                    "username": "name.surname",
                    "email": "name.surname@domain.com",
                    "name": "Name",
                    "surname": "Surname",
                    "is_disabled": False,
                }
            ]
        },
    }


class User(UserBase, table=True):
    """
    Model for User. This model is used to define the table structure.
    Inherits from UserBase.

    \f

    :param id: ID of the user
    :type id: UUID | None
    :param hashed_password: The hashed password
    :type hashed_password: str
    :param created_at: Creation date of the user
    :type created_at: datetime | None
    """

    id: UUID | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class UserCreate(UserBase):
    """
    Model for creating a new user. This model is used to define the fields required for creating a new user.
    Inherits from UserBase.

    \f

    :param hashed_password: The hashed password
    :type hashed_password: str
    """

    hashed_password: str


class UserPublic(UserBase):
    """
    Model for reading a user. This model is used to define the fields returned when reading a user.
    Inherits from UserBase.

    \f

    :param id: ID of the user
    :type id: int
    """

    id: int


class UserUpdate(UserBase):
    """
    Model for updating a user. This model is used to define the fields that can be updated.

    \f

    :param username: Username of the user
    :type username: str
    :param email: Email of the user
    :type email: str
    :param name: Name of the user
    :type name: str | None
    :param surname: Surname of the user
    :type surname: str | None
    :param image_url: User's profile image url
    :type image_url: str | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    username: str | None = Field(default=None, index=True)
    email: str | None = Field(default=None, index=True)
    name: str | None = Field(default=None)
    surname: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    disabled: bool | None = Field(default=None)
