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
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .core.lifespan import lifespan
from .routers import (
    auth,
    songs,
    albums,
    playlists,
    users,
    uploads,
    streams,
    downloads,
)

# load environment variables from the .env file (if present)
load_dotenv()

# access environment variables as if they came from the actual environment
PROJECT_NAME = os.getenv("PROJECT_NAME")

app = FastAPI(
    title=PROJECT_NAME,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # it's faster than JSONResponse
)

# create the public directory if it doesn't exists
os.makedirs("public", exist_ok=True)

# mount the public directory
app.mount("/public", StaticFiles(directory="./public"), name="public")

# setting Jinja2 templates
# we need to create the "templates" directory
templates = Jinja2Templates(directory="./app/templates")

# including all the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(songs.router)
app.include_router(albums.router)
# app.include_router(genres.router)
# app.include_router(artists.router)
app.include_router(playlists.router)
app.include_router(uploads.router)
app.include_router(downloads.router)
app.include_router(streams.router)


@app.get("/", status_code=200)
async def main():
    return {"message": "up and running"}


@app.get("/home", status_code=200)
async def main(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "name": "Mirafy",
            "items": [
                {"value1": "Spotify", "value2": "Clone"},
                {"value1": "by", "value2": "Elia Mirafiori"},
            ],
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=4)
