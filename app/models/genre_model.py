from datetime import datetime

from sqlmodel import Field, SQLModel


class GenreBase(SQLModel):
    """
    Base model for Genre. This model is used to define the common fields.

    \f

    :param name: Name of the genre
    :type name: str
    :param description: Description of the genre
    :type description: str | None
    :param is_disabled: Wheter or not the genre is disabled
    :type is_disabled: bool
    """

    name: str = Field(index=True)
    description: str | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Genre Name",
                    "description": "An genre about...",
                    "is_disabled": False,
                }
            ]
        },
    }


class Genre(GenreBase, table=True):
    """
    Model for Genre. This model is used to define the table structure.
    Inherits from GenreBase.

    \f

    :param id: ID of the genre
    :type id: int | None
    :param created_at: Creation date of the genre
    :type created_at: datetime | None
    """

    id: int | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class GenreCreate(GenreBase):
    """
    Model for creating a new genre. This model is used to define the fields required for creating a new genre.
    Inherits from GenreBase.

    \f
    """

    pass


class GenrePublic(GenreBase):
    """
    Model for reading a genre. This model is used to define the fields returned when reading a genre.
    Inherits from GenreBase.

    \f

    :param id: ID of the genre
    :type id: int
    """

    id: int


class GenreUpdate(GenreBase):
    """
    Model for updating a genre. This model is used to define the fields that can be updated.

    \f

    :param name: Name of the genre
    :type name: str
    :param description: Description of the genre
    :type description: str | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    name: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)
