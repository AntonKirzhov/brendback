from fastapi import APIRouter, Request
from fastapi import Query
from pydantic import BaseModel

from app.schemas.parser import ReadParsersSchema
from app.services.newsletter import send_telegram, create_newsletter, send_email, send_whatsapp, get_history, delete_newsletters

api_router = APIRouter()

class RequestClass(BaseModel):
    name: str
    text: str
    to: str

class HistoryClass(BaseModel):
    user_id: str

class RemoveClass(BaseModel):
    newsletter_ids: list[str]
    user_id: str

@api_router.post("/send_telegram", status_code=200)
async def send_to_telegram(request: Request, item: RequestClass):
    user_id = request.state.user_id
    await send_telegram(item.to, item.text)
    newsletter = await create_newsletter(user_id, item.name, item.to, item.text, "Telegram")
    return newsletter

@api_router.post("/send_email", status_code=200)
async def send_to_email(request: Request, item: RequestClass):
    user_id = request.state.user_id
    await send_email(item.to, item.text)
    newsletter = await create_newsletter(user_id, item.name, item.to, item.text, "Email")
    return newsletter

@api_router.post("/send_whatsapp", status_code=200)
async def send_to_whatsapp(request: Request, item: RequestClass):
    user_id = request.state.user_id
    await send_whatsapp(item.to, item.text)
    newsletter = await create_newsletter(user_id, item.name, item.to, item.text, "Whatsapp")
    return newsletter

@api_router.post("/get_history", status_code=200)
async def get_newsletters_history(request: Request, item: HistoryClass):
    newsletters = await get_history(item.user_id)
    return newsletters

@api_router.post("/delete_newsletter", status_code=200)
async def delete_newsletter(newsletter_ids: str, user_id: str):
    newsletters = await delete_newsletters(user_id, newsletter_ids)
    return newsletters