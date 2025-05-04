from datetime import datetime

from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    """
    Base model for Profile. This model is used to define the common fields.

    \f

    :param Profilename: Profilename of the Profile
    :type Profilename: str
    :param email: Email of the Profile
    :type email: str
    :param name: Name of the Profile
    :type name: str | None
    :param surname: Surname of the Profile
    :type surname: str | None
    :param image_url: Profile's profile image url
    :type image_url: str | None
    :param is_disabled: Wheter or not the Profile is disabled
    :type is_disabled: bool
    """

    Profilename: str
    email: str | None = None
    name: str | None = None
    surname: str | None = None
    image_url: str | None = None
    is_disabled: bool | None = None

    model_config = {
        # "extra": "forbid",  # Otherwise is "allow"
        "json_schema_extra": {
            "examples": [
                {
                    "Profilename": "name.surname",
                    "email": "name.surname@domain.com",
                    "name": "Name",
                    "surname": "Surname",
                    "is_disabled": False,
                }
            ]
        },
    }


class Profile(ProfileBase, table=True):
    """
    Model for Profile. This model is used to define the table structure.
    Inherits from ProfileBase.

    \f

    :param id: ID of the Profile
    :type id: int | None
    :param hashed_password: The hashed password
    :type hashed_password: str
    :param created_at: Creation date of the Profile
    :type created_at: datetime | None
    """

    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class ProfileCreate(ProfileBase):
    """
    Model for creating a new Profile. This model is used to define the fields required for creating a new Profile.
    Inherits from ProfileBase.

    \f

    :param hashed_password: The hashed password
    :type hashed_password: str
    """

    hashed_password: str


class ProfilePublic(ProfileBase):
    """
    Model for reading a Profile. This model is used to define the fields returned when reading a Profile.
    Inherits from ProfileBase.

    \f

    :param id: ID of the Profile
    :type id: int
    """

    id: int


class ProfileUpdate(ProfileBase):
    """
    Model for updating a Profile. This model is used to define the fields that can be updated.

    \f

    :param Profilename: Profilename of the Profile
    :type Profilename: str
    :param email: Email of the Profile
    :type email: str
    :param name: Name of the Profile
    :type name: str | None
    :param surname: Surname of the Profile
    :type surname: str | None
    :param image_url: Profile's profile image url
    :type image_url: str | None
    :param is_disabled: Wheter or not the Profile is disabled
    :type is_disabled: bool
    """

    Profilename: str | None = Field(default=None, index=True)
    email: str | None = Field(default=None, index=True)
    name: str | None = Field(default=None)
    surname: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    disabled: bool | None = Field(default=None)
