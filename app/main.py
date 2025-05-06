"""
Spotify clone by Elia Mirafiori

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

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from .core.lifespan import lifespan
from .routers import (
    auth,
    songs,
    albums,
    genres,
    artists,
    users,
    uploads,
    streams,
    downloads,
)

app = FastAPI(
    title="Spotify Clone",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # it's faster than JSONResponse
)

# create the public directory if it doesn't exists
os.makedirs("public", exist_ok=True)

# mount the public directory
app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(songs.router)
app.include_router(albums.router)
app.include_router(genres.router)
app.include_router(artists.router)
app.include_router(uploads.router)
app.include_router(downloads.router)
app.include_router(streams.router)


@app.get("/", status_code=200)
async def main():
    return {"message": "up and running"}


if __name__ == "__main__":
    pass
