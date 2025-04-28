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


from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .core.lifespan import lifespan
from .routers import auth, items, users

app = FastAPI(
    title="Spotify Clone",
    lifespan=lifespan,
    default_response_class=ORJSONResponse, # it's faster than JSONResponse
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)


@app.get("/", status_code=200)
async def root():
    return {"msg": "Hello World!"}