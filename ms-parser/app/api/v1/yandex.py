
from fastapi import APIRouter, Request, UploadFile

from app.schemas.parser import ReadParsersSchema
from app.schemas.yandex import OrganizationSearchQuery
from app.services import yandex

api_router = APIRouter()


@api_router.post("/get_organizations", status_code=200)
async def retrieve_yandex_organizations(request: Request, search_data: OrganizationSearchQuery):
    user_id = request.state.user_id
    return await yandex.get_all_organizations(search_data, user_id)

@api_router.post("/create_ad_company", status_code=200)
async def create_ad_company(company_name: str, url: str, titles: list[str], texts: list[str], images: list[UploadFile], videos: list[UploadFile], fast_urls: dict, region: str, call_shedule: str, auditory: str, weekly_budget: int, metrica: str = "", target_actions: str = ""):
    return 200