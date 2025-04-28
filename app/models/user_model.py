from datetime import datetime

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """
    Base model for User. This model is used to define the common fields.

    \f

    :param username: Username of the user
    :type username: str
    :param email: Email of the user
    :type email: str
    :param full_name: Full name of the user
    :type full_name: str
    :param disabled: Wheter or not the user is disabled
    :type disabled: bool
    """

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    model_config = {
        # "extra": "forbid",  # Otherwise is "allow"
        "json_schema_extra": {
            "examples": [
                {
                    "username": "name.surname",
                    "email": "name.surname@domain.com",
                    "full_name": "Name Surname",
                    "disabled": False,
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
    :type id: int | None
    :param hashed_password: The hashed password
    :type hashed_password: str
    :param created_at: Creation date of the user
    :type created_at: datetime | None
    """

    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class UserCreate(UserBase):
    """
    Model for creating a new user. This model is used to define the fields required for creating a new hero.
    Inherits from UserBase.

    \f

    :param hashed_password: The hashed password
    :type hashed_password: str
    """

    hashed_password: str


class UserPublic(UserBase):
    """
    Model for reading a user. This model is used to define the fields returned when reading a hero.
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
    :param full_name: Full name of the user
    :type full_name: str
    :param disabled: Wheter or not the user is disabled
    :type disabled: bool
    """

    username: str | None = Field(default=None, index=True)
    email: str | None = Field(default=None, index=True)
    full_name: str | None = Field(default=None)
    disabled: bool | None = Field(default=None)