from typing import Annotated, Any

from fastapi import (
	APIRouter,
	HTTPException,
	Depends,
	Security,
	Path,
	Body,
)
from sqlmodel import (
	Session,
	select,
)

from ..models.song_model import (
	Song,
	SongCreate,
	SongPublic,
	SongUpdate,
)
from ..core.database import get_session
from ..core.auth_utils import get_current_active_user

from ..commons.enums import Scope
from ..commons.common_query_params import CommonQueryParams
# from ..crud.songs import

# dependency injection to get the current user session
SessionDep = Annotated[Session, Depends(get_session)]

# create router for songs
router = APIRouter(
	prefix="/songs", # router prefix url
	tags=["songs"], # router tag
)

@router.post(
	"/", # endpoint url after the prefix specified earlier
	dependencies=[Security(get_current_active_user, scopes=[Scope.ITEMS_CREATE])], # security check, user needs to have permissions to interact with this endpoint
	response_model=SongPublic, # the model used to format the response
	status_code=201, # HTTP status code returned if no errors occur
)
async def post_song(
	session: SessionDep, # request must pass a JWT, with this dependency we extract its data to verify the user
	song: Annotated[SongCreate, Body()], # request must pass a Body with SongCreate fields 
) -> Any: # returns Any because it gets overrided by the response_model
	"""
	Create a new song.

	\f

	:param session: SQLModel session
	:type session: Session
	:param song: Song Body that needs to be posted on DB
	:type song: SongCreate
	:return: The new created Song
	:rtype: SongPublic
	"""
	...

