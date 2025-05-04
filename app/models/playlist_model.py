from datetime import datetime

from sqlmodel import Field, SQLModel


class PlaylistBase(SQLModel):
    """
    Base model for Playlist. This model is used to define the common fields.

    \f

    :param name: Name of the playlist
    :type name: str
    :param description: Description of the playlist
    :type description: str | None
    :param image_url: Playlist's image url
    :type image_url: str | None
    :param user_id: Playlist owner's ID
    :type user_id: str | None
    :param is_disabled: Wheter or not the playlist is disabled
    :type is_disabled: bool
    """

    name: str = Field(index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    user_id: str | None = Field(default=None, foreign_key="user.id")
    is_disabled: bool | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Playlist Name",
                    "description": "An playlist about...",
                    "image_url": "http://...",
                    "user_id": "ABC-123-ABC",
                    "is_disabled": False,
                }
            ]
        },
    }


class Playlist(PlaylistBase, table=True):
    """
    Model for Playlist. This model is used to define the table structure.
    Inherits from PlaylistBase.

    \f

    :param id: ID of the playlist
    :type id: int | None
    :param created_at: Creation date of the playlist
    :type created_at: datetime | None
    """

    id: int | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class PlaylistCreate(PlaylistBase):
    """
    Model for creating a new playlist. This model is used to define the fields required for creating a new playlist.
    Inherits from PlaylistBase.

    \f
    """

    pass


class PlaylistPublic(PlaylistBase):
    """
    Model for reading a playlist. This model is used to define the fields returned when reading a playlist.
    Inherits from PlaylistBase.

    \f

    :param id: ID of the playlist
    :type id: int
    """

    id: int


class PlaylistUpdate(PlaylistBase):
    """
    Model for updating a playlist. This model is used to define the fields that can be updated.

    \f

    :param name: Name of the playlist
    :type name: str
    :param description: Description of the playlist
    :type description: str | None
    :param image_url: Playlist's image url
    :type image_url: str | None
    :param user_id: Playlist owner's ID
    :type user_id: str | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    name: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    user_id: str | None = Field(default=None, foreign_key="user.id")
    is_disabled: bool | None = Field(default=None)
