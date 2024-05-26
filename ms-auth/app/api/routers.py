from fastapi import APIRouter

from app.api.v1.users import user_routes
from app.api.v1.projects import project_routes
from app.api.v1.media import media
from app.api.v1.audioclips import audioclips
from app.api.v1.companies import companies
from app.api.v1.notifications import notifications

v1_router = APIRouter(prefix='/api/v1')

v1_router.include_router(user_routes, prefix='/users', tags=['users_auth'])
v1_router.include_router(media, prefix="/media", tags=["media"])
v1_router.include_router(project_routes, prefix='/projects', tags=['projects'])
v1_router.include_router(audioclips, prefix='/audioclips', tags=['audioclips'])
v1_router.include_router(companies, prefix='/companies', tags=['companies'])
v1_router.include_router(notifications, prefix='/notifications', tags=['notifications'])