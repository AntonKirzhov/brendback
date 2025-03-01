from fastapi import APIRouter, Request
from fastapi import Query

from app.enums.region import AvitoRegion
from app.enums.category import AvitoCategory

from app.schemas.avito import AvitoParserData
from app.schemas.parser import ReadParsersSchema
from app.services.avito import get_all

api_router = APIRouter()


@api_router.post("/get_data", status_code=200)
async def get_avito_data(
    request: Request,
    body: AvitoParserData,
    region: AvitoRegion = AvitoRegion.All,
    category: AvitoCategory = AvitoCategory.TRANSPORT,
    limit: int = Query(default=0, ge=1, le=100),
):
    fields = body.fields
    user_id = request.state.user_id
    all_data = await get_all(fields, region, category, user_id, limit)
    return all_data
