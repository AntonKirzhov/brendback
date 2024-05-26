import typing as tp
import os

from fastapi import APIRouter, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app import services

companies = APIRouter()

@companies.get("/companies_main/", status_code=200)
async def get_main_companies(user_id: str):
    return await services.list_main_companies(user_id)

@companies.get("/companies_list/", status_code=200)
async def list_companies(user_id: str):
    return await services.list_companies(user_id)

@companies.get("/companies_get/", status_code=200)
async def get_company_by_id(user_id: str, company_id: str):
    return await services.get_company_by_id(user_id, company_id)

@companies.post("/companies_create/", status_code=200)
async def create_company(user_id: str, company_name: str, official_address: str, official_requisites: str, goods: str, is_services: str, technologies: str, health: str, education: str, production: str, transportation: str, company_region: str, company_city: str, company_urls: str, facebook: str, vk: str, tiktok: str, telegram: str, instagram: str):
    return await services.create_company(user_id, company_name, official_address, official_requisites, goods, is_services, technologies, health, education, production, transportation, company_region, company_city, company_urls, facebook, vk, tiktok, telegram, instagram)

@companies.post("/companies_update/", status_code=200)
async def create_company(user_id: str, company_id: str, company_name: str, official_address: str, official_requisites: str, goods: str, is_services: str, technologies: str, health: str, education: str, production: str, transportation: str, company_region: str, company_city: str, company_urls: str, facebook: str, vk: str, tiktok: str, telegram: str, instagram: str):
    return await services.update_company(user_id, company_id, company_name, official_address, official_requisites, goods, is_services, technologies, health, education, production, transportation, company_region, company_city, company_urls, facebook, vk, tiktok, telegram, instagram)

@companies.post("/companies_delete/", status_code=200)
async def delete_company(user_id: str, company_id: str):
    return await services.delete_company(user_id, company_id)