from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class ArtistBase(SQLModel):
    """
    Base model for Artist. This model is used to define the common fields.

    \f

    :param name: Name of the artist
    :type name: str
    :param description: Description of the artist
    :type description: str | None
    :param image_url: Artist's image url
    :type image_url: str | None
    :param is_disabled: Wheter or not the artist is disabled
    :type is_disabled: bool
    """

    name: str = Field(index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Artist Name",
                    "description": "An artist that...",
                    "image_url": "http://...",
                    "is_disabled": False,
                }
            ]
        },
    }


class Artist(ArtistBase, table=True):
    """
    Model for Artist. This model is used to define the table structure.
    Inherits from ArtistBase.

    \f

    :param id: ID of the artist
    :type id: UUID | None
    :param released_at: Release date of the artist
    :type released_at: datetime | None
    :param created_at: Creation date of the artist
    :type created_at: datetime | None
    """

    id: UUID | None = Field(default=None, primary_key=True, index=True)
    released_at: datetime | None = Field(default=datetime.now(), index=True)
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class ArtistCreate(ArtistBase):
    """
    Model for creating a new artist. This model is used to define the fields required for creating a new artist.
    Inherits from ArtistBase.

    \f
    """

    pass


class ArtistPublic(ArtistBase):
    """
    Model for reading a artist. This model is used to define the fields returned when reading a artist.
    Inherits from ArtistBase.

    \f

    :param id: ID of the artist
    :type id: UUID
    """

    id: UUID


class ArtistUpdate(ArtistBase):
    """
    Model for updating a artist. This model is used to define the fields that can be updated.

    \f

    :param name: Name of the artist
    :type name: str
    :param description: Description of the artist
    :type description: str | None
    :param image_url: Artist's image url
    :type image_url: str | None
    :param released_at: Release date of the artist
    :type released_at: datetime | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    name: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    released_at: datetime | None = Field(default=datetime.now(), index=True)
    is_disabled: bool | None = Field(default=None)
