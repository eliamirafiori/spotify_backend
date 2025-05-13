from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlmodel import Session, select

from ..commons.common_query_params import CommonQueryParams
from ..models.playlist_model import (
    Playlist,
    PlaylistCreate,
    PlaylistPublic,
    PlaylistUpdate,
)
from ..models.song_model import Song, SongPublic
from ..models.relationship_song_playlist import SongPlaylistLink


async def create_playlist(
    session: Session,
    playlist: PlaylistCreate,
) -> PlaylistPublic:
    """
    Create a new playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist: Playlist to create
    :type playlist: PlaylistCreate
    :return: Created song
    :rtype: PlaylistPublic
    """
    db_playlist = Playlist.model_validate(playlist)
    session.add(db_playlist)
    session.commit()
    session.refresh(db_playlist)
    return db_playlist


async def read_playlists(
    session: Session,
    user_id: Annotated[int, Body()],
    params: CommonQueryParams = Depends(),
) -> list[PlaylistPublic]:
    """
    Get all playlists with pagination.

    \f

    :param session: SQLModel session
    :type session: Session
    :param user_id: User's ID to find his playlists
    :type user_id: int
    :param params: Common parameters for pagination
    :type params: CommonParams
    :return: List of songs
    :rtype: list[PlaylistPublic]
    """
    return session.exec(
        select(Playlist)
        .where(Playlist.user_id == user_id)
        .offset(params.offset)
        .limit(params.limit)
    ).all()


async def read_playlist(
    session: Session,
    id: Annotated[int, Body()],
    user_id: Annotated[int, Body()],
) -> PlaylistPublic | None:
    """
    Get specific playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: String to filter on
    :type id: int
    :param user_id: User's ID to find his playlist
    :type user_id: int
    :return: Playlist or None
    :rtype: PlaylistPublic | None
    """

    return session.exec(
        select(Playlist).where(Playlist.id == id, Playlist.user_id == user_id)
    ).first()


async def read_playlist_songs(
    session: Session,
    id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Get playlist's songs.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Playlist's ID
    :type id: int
    :return: List of the playlist's songs
    :rtype: list[SongPublic]
    """
    # check if playlist exists
    db_playlist = session.get(Playlist, id)  # get the existing playlist instance
    if not db_playlist:  # check if the playlist exists
        raise HTTPException(status_code=404, detail="Playlist not found")

    # Query songs associated with the playlist
    statement = select(Song).join(SongPlaylistLink)
    return session.exec(statement).all()


async def update_playlist(
    session: Session,
    id: int,
    playlist: PlaylistUpdate,
) -> PlaylistPublic:
    """
    Update specific playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Playlist's ID
    :type id: int
    :param playlist: The playlist's data
    :type playlist: PlaylistCreate
    :return: Playlist instance
    :rtype: PlaylistPublic
    """
    db_playlist = session.get(Playlist, id)  # get the existing playlist instance
    if not db_playlist:  # check if the playlist exists
        raise HTTPException(status_code=404, detail="Playlist not found")

    playlist_data = playlist.model_dump(exclude_unset=True)  # get only updated values
    for key, value in playlist_data.items():  # iterate through playlist's data
        # map key and value from playlist's data to its db instance
        setattr(db_playlist, key, value)

    session.add(db_playlist)  # add the updated version to the DB
    session.commit()  # commit the cheanges to the DB
    session.refresh(db_playlist)  # refresh the db_song instance
    return db_playlist


async def delete_playlist(
    session: Session,
    id: int,
) -> None:
    """
    Delete specific playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param id: Playlist's ID
    :type id: int
    :return: Nothing, as expected when returning STATUS CODE 204
    :rtype: None
    """
    db_playlist = session.get(Playlist, id)  # get the existing playlist instance
    if not db_playlist:  # check if the playlist exists
        raise HTTPException(status_code=404, detail="Playlist not found")

    session.delete(db_playlist)  # delete the instance of the playlist
    session.commit()  # commit the changes to the DB


async def create_playlist_song_link(
    session: Session,
    playlist_id: Annotated[int, Body()],
    song_id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Add a song to a playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :param song_id: Song's ID
    :type song_id: int
    :return: List of songs contained in the playlist
    :rtype: list[SongPublic]
    """
    # check if playlist exists
    db_playlist = session.get(
        Playlist, playlist_id
    )  # get the existing playlist instance
    if not db_playlist:  # check if the playlist exists
        raise HTTPException(status_code=404, detail="Playlist not found")

    # check if song exists
    db_song = session.get(Song, song_id)  # get the existing song instance
    if not db_song:  # check if the song exists
        raise HTTPException(status_code=404, detail="Song not found")

    # check if link exists
    db_link = session.exec(
        select(SongPlaylistLink).where(
            SongPlaylistLink.playlist_id == playlist_id,
            SongPlaylistLink.song_id == song_id,
        )
    ).fist()  # get the existing link instance
    if db_link:  # check if the link exists
        raise HTTPException(
            status_code=404, detail="Relationship between Song and Playlist found"
        )

    data_link: SongPlaylistLink = SongPlaylistLink(
        playlist_id=playlist_id, song_id=song_id
    )
    session.add(data_link)
    session.commit()

    return read_playlist_songs(session=session, id=playlist_id)


async def delete_playlist_song_link(
    session: Session,
    playlist_id: Annotated[int, Body()],
    song_id: Annotated[int, Body()],
) -> list[SongPublic]:
    """
    Remove a song from a playlist.

    \f

    :param session: SQLModel session
    :type session: Session
    :param playlist_id: Playlist's ID
    :type playlist_id: int
    :param song_id: Song's ID
    :type song_id: int
    :return: List of songs contained in the playlist
    :rtype: list[SongPublic]
    """
    # check if playlist exists
    db_playlist = session.get(
        Playlist, playlist_id
    )  # get the existing playlist instance
    if not db_playlist:  # check if the playlist exists
        raise HTTPException(status_code=404, detail="Playlist not found")

    # check if song exists
    db_song = session.get(Song, song_id)  # get the existing song instance
    if not db_song:  # check if the song exists
        raise HTTPException(status_code=404, detail="Song not found")

    # check if link exists
    db_link = session.exec(
        select(SongPlaylistLink).where(
            SongPlaylistLink.playlist_id == playlist_id,
            SongPlaylistLink.song_id == song_id,
        )
    ).fist()  # get the existing link instance
    if not db_link:  # check if the link exists
        raise HTTPException(
            status_code=404, detail="Relationship between Song and Playlist not found"
        )

    session.delete(db_link)
    session.commit()

    return read_playlist_songs(session=session, id=playlist_id)
