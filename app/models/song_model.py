from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class SongBase(SQLModel):
    """
    Song model for User. This model is used to define the common fields.

    \f

    :param song_url: Song's url
    :type song_url: str
    :param title: Title of the song
    :type title: str
    :param description: description of the song
    :type description: str | None
    :param image_url: Song's image url
    :type image_url: str | None
    :param album_id: Song's album ID, None if it's a single
    :type album_id: str | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    song_url: str = Field()
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    album_id: str | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "song_url": "http://...",
                    "title": "name.surname@domain.com",
                    "description": "A song about...",
                    "image_url": "http://...",
                    "album_id": "ABC-123-ABC",
                    "is_disabled": False,
                }
            ]
        },
    }


class Song(SongBase, table=True):
    """
    Model for Song. This model is used to define the table structure.
    Inherits from SongBase.

    \f

    :param id: ID of the song
    :type id: UUID | None
    :param created_at: Creation date of the user
    :type created_at: datetime | None
    """

    id: UUID | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime | None = Field(default=datetime.now(), index=True)


class SongCreate(SongBase):
    """
    Model for creating a new song. This model is used to define the fields required for creating a new song.
    Inherits from SongBase.

    \f
    """

    pass


class SongPublic(SongBase):
    """
    Model for reading a song. This model is used to define the fields returned when reading a song.
    Inherits from SongBase.

    \f

    :param id: ID of the song
    :type id: UUID
    """

    id: UUID


class SongUpdate(SongBase):
    """
    Model for updating a song. This model is used to define the fields that can be updated.

    \f

    :param title: Title of the song
    :type title: str
    :param description: description of the song
    :type description: str | None
    :param image_url: Song's image url
    :type image_url: str | None
    :param album_id: Song's album ID, None if it's a single
    :type album_id: str | None
    :param is_disabled: Wheter or not the user is disabled
    :type is_disabled: bool
    """

    title: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None)
    album_id: str | None = Field(default=None)
    is_disabled: bool | None = Field(default=None)
