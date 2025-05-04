from datetime import datetime
from sqlmodel import SQLModel, Field

from .song_model import Song
from .genre_model import Genre


class SongGenre(SQLModel, table=True):
    """
    Relatioship between Song and Genre.

    \f

    :param song_id: ID of the song
    :type song_id: str
    :param genre_id: ID of the genre
    :type genre_id: str
    :param created_at: Creation date of the relationship
    :type created_at: datetime | None
    """

    song_id: int = Field(
        default=None,
        foreign_key="song.id",
        primary_key=True,
        index=True,
    )
    genre_id: int = Field(
        default=None,
        foreign_key="genre.id",
        primary_key=True,
        index=True,
    )
    created_at: datetime | None = Field(default=datetime.now(), index=True)

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "examples": [
                {
                    "song_id": "ABC-123-ABC",
                    "genre_id": "ABC-321-ABC",
                }
            ]
        },
    }
