import typing as tp
import os

from fastapi import APIRouter, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app import services

notifications = APIRouter()

@notifications.get("/notification_list/", status_code=200)
async def list_notifications(user_id: str, limit: int = 0):
    return await services.list_notifications(user_id, limit)

@notifications.post("/notification_add/", status_code=200)
async def add_notification(user_id: str, text: str, source: str):
    return await services.add_notification(user_id, text, source)

@notifications.post("/notification_delete/", status_code=200)
async def delete_notification(user_id: str, notification_id: str):
    return await services.delete_notification(user_id, notification_id)

@notifications.post("/notifications_clear/", status_code=200)
async def clear_notifications(user_id: str, limit: int = 0):
    return await services.clear_notifications(user_id, limit)

'''@audioclips.post("/clip_create/", status_code=200)
async def create_audioclip(user_id: str, clip_name: str, clip_description: str, file: UploadFile):
    return await services.create_audioclip(user_id, clip_name, clip_description, file)

@audioclips.post("/clip_delete/", status_code=200)
async def delete_audioclip(user_id: str, clip_id: str):
    return await services.delete_audioclip(user_id, clip_id)

@audioclips.get("/call_list/", status_code=200)
async def list_calls(user_id: str):
    return await services.list_calls(user_id)

@audioclips.post("/call_create/", status_code=200)
async def create_call(user_id: str, call_name: str, audioclip_id: str, phones: list[str]):
    return await services.create_call(user_id, call_name, audioclip_id, phones)

@audioclips.post("/call_delete/", status_code=200)
async def delete_call(user_id: str, call_id: str):
    return await services.delete_call(user_id, call_id)'''