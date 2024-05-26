import typing as tp
import os

from fastapi import APIRouter, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app import services
from app.schemas import (
    AudioclipCreate as AudioclipCreateSchema,
)

audioclips = APIRouter()

@audioclips.get("/clip_list/", status_code=200)
async def list_audioclips(user_id: str):
    return await services.list_audioclips(user_id)

@audioclips.post("/clip_create/", status_code=200)
async def create_audioclip(user_id: str, clip_name: str, clip_description: str, file: UploadFile):
    return await services.create_audioclip(user_id, clip_name, clip_description, file)

@audioclips.post("/clip_delete/", status_code=200)
async def delete_audioclip(user_id: str, clip_id: str):
    return await services.delete_audioclip(user_id, clip_id)

@audioclips.post("/clip_get/", status_code=200)
async def get_audioclip(audioclip_id: str):
    return await services.get_audioclip(audioclip_id)

@audioclips.get("/call_list/", status_code=200)
async def list_calls(user_id: str):
    return await services.list_calls(user_id)

@audioclips.post("/call_create/", status_code=200)
async def create_call(user_id: str, call_name: str, audioclip_id: str, phones: list[str]):
    return await services.create_call(user_id, call_name, audioclip_id, phones)

@audioclips.post("/call_delete/", status_code=200)
async def delete_call(user_id: str, call_id: str):
    return await services.delete_call(user_id, call_id)