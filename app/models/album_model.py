from datetime import datetime

from sqlmodel import Field, SQLModel


class AlbumBase(SQLModel):
    """
    Base model for Album. This model is used to define the common fields.

    \f

    :param title: Title of the album
    :type title: str
    :param description: Description of the album
    :type description: str | None
    :param image_url: Album's image url
    :type image_url: str | None
    :param is_disabled: Wheter or not the album is disabled
    :type is_disabled: bool
    """

    title: str = Field(index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Album Title",
                    "description": "An album about...",
                    "image_url": "http://...",
                    "is_disabled": False,
                }
            ]
        },
    }


class Album(AlbumBase, table=True):
    """
    Model for Album. This model is used to define the table structure.
    Inherits from AlbumBase.

    \f

    :param id: ID of the album
    :type id: int | None
    :param released_at: Release date of the album
    :type released_at: datetime | None
    :param created_at: Creation date of the album
    :type created_at: datetime | None
    """

    id: int | None = Field(default=None, primary_key=True, index=True)
    released_at: datetime | None = Field(default=datetime.now(), index=True)
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class AlbumCreate(AlbumBase):
    """
    Model for creating a new album. This model is used to define the fields required for creating a new album.
    Inherits from AlbumBase.

    \f
    """

    released_at: datetime | None = None


class AlbumPublic(AlbumBase):
    """
    Model for reading a album. This model is used to define the fields returned when reading a album.
    Inherits from AlbumBase.

    \f

    :param id: ID of the album
    :type id: int
    """

    id: int


class AlbumUpdate(AlbumBase):
    """
    Model for updating a album. This model is used to define the fields that can be updated.

    \f

    :param title: Title of the album
    :type title: str
    :param description: Description of the album
    :type description: str | None
    :param image_url: Album's image url
    :type image_url: str | None
    :param released_at: Release date of the album
    :type released_at: datetime | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    title: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    released_at: datetime | None = Field(default=None, index=True)
    is_disabled: bool | None = Field(default=None)
