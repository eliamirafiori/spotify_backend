"""
Ticketing System

For licences check: https://en.wikipedia.org/wiki/Software_license
"""

__author__ = "Elia Mirafiori"
__authors__ = "Elia Mirafiori"
__contact__ = "el.mirafiori@gmail.com"
__copyright__ = "Copyright © 2025 Elia Mirafiori"
__license__ = "GPLv3"
__date__ = "28 Apr 2025"
__version__ = "1.0.0"

import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import ORJSONResponse, StreamingResponse, Response, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .core.lifespan import lifespan
from .routers import auth, songs, albums, users, uploads, streams, downloads

app = FastAPI(
    title="Spotify Clone",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # it's faster than JSONResponse
)

app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(songs.router)
app.include_router(albums.router)
app.include_router(uploads.router)
app.include_router(downloads.router)
app.include_router(streams.router)


@app.get("/")
async def main():
    content = """
<body>
<form action="/songs/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.get("/video")
def video():
    def iterfile():
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )  # get the directory of the current file
        print(f"BASE DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIR: {base_dir}")
        video_path = os.path.join(
            base_dir, "..", "public/video/large_video.mp4"
        )  # construct the absolute path to the video file

        print(f"VIDEO DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIR: {video_path}")
        with open(video_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.get("/video2")
async def video2(request: Request):
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # Get the directory of this file
    video_path = os.path.join(
        base_dir, "..", "public/video/large_video.mp4"
    )  # Construct the absolute path

    try:
        file_size = os.path.getsize(video_path)
        range_header = request.headers.get("range")
        if range_header:
            # Parse the Range header
            range_start, range_end = range_header.replace("bytes=", "").split("-")
            range_start = int(range_start)
            range_end = int(range_end) if range_end else file_size - 1

            if range_start >= file_size or range_end >= file_size:
                raise HTTPException(
                    status_code=416, detail="Requested Range Not Satisfiable"
                )

            chunk_size = range_end - range_start + 1
            with open(video_path, "rb") as video_file:
                video_file.seek(range_start)
                data = video_file.read(chunk_size)

            headers = {
                "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(chunk_size),
                "Content-Type": "video/mp4",
            }
            return StreamingResponse(data, status_code=206, headers=headers)

        # If no Range header, return the entire file
        with open(video_path, "rb") as video_file:
            data = video_file.read()

        headers = {
            "Content-Length": str(file_size),
            "Content-Type": "video/mp4",
        }
        return StreamingResponse(data, headers=headers)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video file not found")


@app.get("/audio")
def audio():
    def iterfile():
        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )  # get the directory of the current file
        print(f"BASE DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIR: {base_dir}")
        video_path = os.path.join(
            base_dir, "..", "public/audio/audio_1.mp3"
        )  # construct the absolute path to the audio file

        print(f"VIDEO DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIR: {video_path}")
        with open(video_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile())


@app.get("/audio2")
async def audio2(request: Request):
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # Get the directory of this file
    audio_path = os.path.join(
        base_dir, "..", "public/audio/audio_1.mp3"
    )  # Construct the absolute path

    try:
        file_size = os.path.getsize(audio_path)
        range_header = request.headers.get("range")
        if range_header:
            # Parse the Range header
            range_start, range_end = range_header.replace("bytes=", "").split("-")
            range_start = int(range_start)
            range_end = int(range_end) if range_end else file_size - 1

            if range_start >= file_size or range_end >= file_size:
                raise HTTPException(
                    status_code=416, detail="Requested Range Not Satisfiable"
                )

            chunk_size = range_end - range_start + 1
            with open(audio_path, "rb") as audio_file:
                audio_file.seek(range_start)
                data = audio_file.read(chunk_size)

            headers = {
                "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(chunk_size),
                "Content-Type": "audio/mpeg",
            }
            return Response(data, status_code=206, headers=headers)

        # If no Range header, return the entire file
        with open(audio_path, "rb") as audio_file:
            data = audio_file.read()

        headers = {
            "Content-Length": str(file_size),
            "Content-Type": "audio/mpeg",
        }
        return Response(data, headers=headers)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Audio file not found")
