from datetime import datetime
from typing import Annotated, Any, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Path, Cookie, Header
from fastapi.responses import ORJSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel, EmailStr, constr


class CommonCookies(BaseModel):
    # session_id: Annotated[str, Cookie()]
    # facebook_tracker: Annotated[str | None, Cookie()] = None
    # google_tracker: Annotated[str | None, Cookie()] = None
    session_id: str
    facebook_tracker: str | None = None
    google_tracker: str | None = None
