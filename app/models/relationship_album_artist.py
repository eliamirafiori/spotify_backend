from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field

from .album_model import Album
from .artist_model import Artist


class AlbumArtist(SQLModel, table=True):
    """
    Relatioship between Album and Artist.

    \f

    :param album_id: ID of the album
    :type album_id: str
    :param artist_id: ID of the artist
    :type artist_id: str
    :param created_at: Creation date of the relationship
    :type created_at: datetime | None
    """

    album_id: UUID = Field(
        default=None,
        foreign_key="album.id",
        primary_key=True,
        index=True,
    )
    artist_id: UUID = Field(
        default=None,
        foreign_key="artist.id",
        primary_key=True,
        index=True,
    )
    created_at: datetime | None = Field(default=datetime.now(), index=True)

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "examples": [
                {
                    "album_id": "ABC-123-ABC",
                    "artist_id": "ABC-321-ABC",
                }
            ]
        },
    }
