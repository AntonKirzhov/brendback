import os
import json
import uuid
import secrets
import aiofiles
import aiohttp
import mimetypes
import typing as tp

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

from datetime import datetime, timedelta
from bson import ObjectId
from passlib.context import CryptContext

from app.config import settings
from app.repositories import UsersRepository, ProjectsRepository
from app.schemas import (
    Token as TokenSchema,
    Login as LoginSchema,
    RefreshToken as RefreshTokenSchema,
    Email as EmailSchema,
    ResetPasswords as ResetPasswordsSchema,
    RetrieveLogin as RetrieveLoginSchema,
    AudioclipCreate as AudioclipCreateSchema,
)
from app import services
from app.schemas.users import PatchUserUpdateRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def append_to_json_file(file_name, expire_date, _id, secure_number):
    try:
        with open(file_name, "r") as file:
            data = dict(json.load(file))

        data[secure_number] = [expire_date, _id]
        with open(file_name, "w") as file:
            json.dump(data, file)
    except FileNotFoundError:
        data_test = []
        with open(file_name, "w") as file:
            json.dump(data_test, file)


async def read_secure_number(file_name, secure_number):
    # TODO refactor
    with open(file_name, "r") as file:
        data = json.load(file)

    if secure_number not in data:
        raise HTTPException(status_code=409, detail="Invalid secure number.")

    expire_date, _id = data[secure_number]
    if datetime.now() > datetime.fromisoformat(expire_date):
        raise HTTPException(status_code=409, detail="Secure number has expired.")
    return _id


async def get_user_by_id(user_id: str) -> dict:
    return await UsersRepository().get_by_id(_id=user_id)  # type: ignore


async def save_user_avatar_image(
    user_id: str, file: UploadFile
) -> tp.Dict[str, tp.Any]:
    try:
        user = await get_user_by_id(user_id=user_id)
        if len(user) > 0 and user['avatar_link'] != "none":
            file_path = user["avatar_link"]
            if os.path.exists(file_path):
                os.remove(file_path)

        media_path = os.path.join("media", "userdata", "avatars")
        if not os.path.exists(media_path):
            os.makedirs(media_path)

        unique_filename = str(uuid.uuid4()).replace('-', '')

        content_type, _ = mimetypes.guess_type(str(file.filename))
        if content_type is None or not content_type.startswith("image"):
            file_extension = "jpg"
        else:
            file_extension = str(mimetypes.guess_extension(content_type))
            if file_extension:
                file_extension = file_extension[1:]

        file_name = f"{unique_filename}.{file_extension}"
        file_path = os.path.join("media/userdata/avatars", file_name)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        file_path = file_path.replace("\\", "/")

        await UsersRepository().update_user_avatar_link(_id=user_id, avatar_link=file_path)

        image_link = f"{settings.SERVICE_URL}/{file_path}/"
        return {"avatar_link": image_link}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


async def select_company(user_id: str, company_id: str):
    try:
        if company_id != "-":
            company = await UsersRepository().get_user_company_by_id(company_id=company_id)
            if len(company) <= 0:
                raise HTTPException(status_code=404, detail="Компания с таким ID не найдена.")
            company = company[0]
            if str(company['user_id']) != str(user_id):
                raise HTTPException(status_code=405, detail="Пользователь не является владельцем этой компании.")

        await UsersRepository().change_company_by_id(_id=user_id, company_id=company_id)
        return 200
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

async def update_user(user_id: str, instance: PatchUserUpdateRequest):
    data = instance.dict(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="Bad request.")

    await UsersRepository().update_by_id(_id=user_id, data=data)
    return await UsersRepository().get_by_id(_id=user_id)


async def get_all():
    return await UsersRepository().get_all()


async def create_user(person) -> dict:
    user = await UsersRepository().get_by_email(email=person.email)
    if len(user) > 0:
        raise HTTPException(
            status_code=409, detail="User with such email already exists"
        )
    secure_number = secrets.randbelow(1000000)
    secure_number_str = f"{secure_number:06}"
    print(secure_number_str)

    await services.send_mail(
        email=person.email,
        content=f"{await services.open_html(str(person.email), 'Пользователь', secure_number_str, False, True)}",
    )
    returned = await UsersRepository().create(instance=person.dict())
    await UsersRepository().update_email_code(email=person.email, code=secure_number_str)
    return returned

async def create_legal_user(person) -> dict:
    user = await UsersRepository().get_by_email(email=person.email)
    if len(user) > 0:
        raise HTTPException(
            status_code=409, detail="User with such email already exists"
        )
    secure_number = secrets.randbelow(1000000)
    secure_number_str = f"{secure_number:06}"
    print(secure_number_str)

    await services.send_mail(
        email=person.email,
        content=f"{await services.open_html(str(person.email), 'Пользователь', secure_number_str, False, True)}",
    )
    returned = await UsersRepository().create_legal(instance=person.dict())
    await UsersRepository().update_email_code(email=person.email, code=secure_number_str)
    return returned

async def login_user(data: LoginSchema) -> TokenSchema:
    user = await UsersRepository().get_by_email(email=data.email)
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="No such user with chosen email.")
    user = user[0]
    if data.password != user['password']:
        raise HTTPException(status_code=401, detail="Incorrect credentials.")

    tokens = await services.create_tokens(user_id=str(user['_id']))
    return RetrieveLoginSchema(user=user, **tokens.dict())


async def check_exist_company_by_inn(inn: str) -> dict:
    """
    :param inn: INN
    :return: True if there is an entry in the registry with this INN, else return False
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api-fns.ru/api/egr?req={inn}&key=71e92fe3cb0ecc4ed7aee8155080311fb78b47d1"
        ) as response:
            text = await response.text()
            # TODO: Fix the description
            if response.status == 403:
                raise HTTPException(
                    status_code=500,
                    detail=f"ERROR {text}",
                )
            company_exist = await response.json()
            if not 'items' in company_exist or company_exist['items'] == []:
                raise HTTPException(
                    status_code=404, detail="Компания с таким INN не найдена."
                )
            return company_exist['items']


async def collect_additional_info(additional_info: dict):
    data = await check_exist_company_by_inn(tin=additional_info.get("inn", None))
    juridical_person = data[0]["ЮЛ"]
    name = juridical_person["НаимСокрЮЛ"]
    full_name = juridical_person["Руководитель"]["ФИОПолн"]
    address = juridical_person["Адрес"]["АдресПолн"]
    return {"name": name, "head": full_name, "address": address} | additional_info


async def new_ticket(user_id, text):
    user_info = await UsersRepository().get_by_id(_id=user_id)
    if user_info:
        return await services.send_ticket(
            email="slaterpsamp@yandex.ru",
            content=f"Новое обращение от {user_info['first_name']} {user_info['last_name']}<br>#{user_info['_id']}<br>Email: {user_info['email']}<br>Телефон: {user_info['phone']}<br><br>{text}"
        )
    else:
        return 404

async def forgot_password(email: EmailSchema):
    secure_number = secrets.randbelow(1000000)
    secure_number_str = f"{secure_number:06}"
    print(secure_number_str)

    # TODO move to depends
    user = await UsersRepository().get_by_email(email=email.email)
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="No such user with chosen email.")
    user = user[0]
    expire_date = datetime.now() + timedelta(minutes=30)
    await append_to_json_file(
        "reset_passwords.json",
        str(expire_date),
        str(user["_id"]),
        secure_number_str,
    )

    user_first_name = str(user["first_name"])
    await services.send_mail(
        email=email.email,
        content=f"{await services.open_html(str(user['email']), user_first_name, secure_number_str, email.is_change)}",
    )


async def reset_password(data: ResetPasswordsSchema):
    _id = await read_secure_number(
        "reset_passwords.json", secure_number=data.secure_code
    )
    user = await get_user_by_id(user_id=_id)
    await UsersRepository().update_user_password(_id, data.password)


async def activate_person(user_id: str, code: str):
    user = await UsersRepository().get_by_id(_id=user_id)
    if user['is_verified'] == "True":
        return 200
    else:
        if code == user['email_code']:
            await UsersRepository().activate_user(user_id)
            return 200
        else:
            return 409

async def delete_person(user_id: str):
    await UsersRepository().delete_by_id(_id=user_id)
    #await UsersRepository().delete_user_parsers(owner_id=ObjectId(user_id))
    #await ProjectsRepository().delete_all_user_projects(owner_id=ObjectId(user_id))
    return {"result": f"User {user_id} sucessfully deleted"}


async def get_user_by_token(self, authorization: str) -> dict:
    user_id = await self.tokens.decode_access_jwt_token(authorization=authorization)
    return await self.get_user_by_id(user_id=user_id)


async def refresh_token(self, token: RefreshTokenSchema) -> TokenSchema:
    user_id = await self.tokens.decode_refresh_jwt_token(
        refresh_token=token.refresh_token
    )
    return await self.tokens.generate_response(user_id=user_id)


def verify_password(self, *, plain_password: str, hashed_password: str) -> bool:
    return self.pwd_context.verify(plain_password, hashed_password)

async def update_tariff(user_id, tariff):
    return await UsersRepository().update_tariff(_id=user_id, tariff=tariff)

async def list_audioclips(user_id):
    return await UsersRepository().list_audioclips(user_id=user_id)

async def create_audioclip(user_id, clip_name, clip_description, file):
    readed = await file.read()
    async with aiohttp.ClientSession() as session:
        async with session.post("https://zvonok.com/manager/cabapi_external/api/v1/audio/upload/", data={"public_key": "46680aa2d0a4979f45aed876d3bf2f1f", "clip_name": clip_name, "text": clip_description, "clip_file": readed}) as response:
            req_json = await response.json()
            sql = await UsersRepository().create_audioclip(user_id=user_id, zvonok_id=req_json['audioclip_id'], clip_name=clip_name, clip_description=clip_description)
            try:
                async with aiofiles.open(f'/root/DEV/ms-auth/media/audioclips/audio{sql}.mp3', mode='wb') as f:
                    await f.write(readed)
            except Exception as e:
                print(e)
            return response.status

async def get_audioclip(audioclip_id):
    return FileResponse(path=f"/root/DEV/ms-auth/media/audioclips/audio{audioclip_id}.mp3", filename=f"sound.mp3", media_type='multipart/form-data')

async def delete_audioclip(user_id, clip_id):
    await UsersRepository().delete_audioclip(user_id=user_id, clip_id=clip_id)

async def list_calls(user_id):
    return await UsersRepository().list_calls(user_id=user_id)

async def create_call(user_id, call_name, audioclip_id, phones):
    audioclip_id = await UsersRepository().get_audioclip_by_audio(_id=audioclip_id)
    print(audioclip_id)
    await UsersRepository().create_call(user_id=user_id, call_name=call_name, audioclip_id=audioclip_id, phones=phones)
    async with aiohttp.ClientSession() as session:
        for phone in phones:
            async with session.post("https://zvonok.com/manager/cabapi_external/api/v1/phones/call/", data={"public_key": "46680aa2d0a4979f45aed876d3bf2f1f", "phone": phone, "campaign_id": "2043696868", "text": f'<audio id="{audioclip_id}"/>'}) as response:
                print(response.status)
                print(await response.text())

async def delete_call(user_id, call_id):
    await UsersRepository().delete_call(user_id=user_id, call_id=call_id)

async def list_main_companies(user_id):
    result = {
        "companies": await UsersRepository().list_main_companies(user_id=user_id),
        "selected_company": await UsersRepository().get_selected_company_by_user_id(user_id=user_id)
    }

    return result

async def list_companies(user_id):
    return await UsersRepository().list_companies(user_id=user_id)

async def get_company_by_id(user_id, company_id):
    return await UsersRepository().get_company_by_id(user_id=user_id, company_id=company_id)

async def create_company(user_id, company_name, official_address, official_requisites, goods, services, technologies, health, education, production, transportation, company_region, company_city, company_urls, facebook, vk, tiktok, telegram, instagram):
    return await UsersRepository().create_company(user_id, company_name, official_address, official_requisites, goods, services, technologies, health, education, production, transportation, company_region, company_city, company_urls, facebook, vk, tiktok, telegram, instagram)

async def update_company(user_id, company_id, company_name, official_address, official_requisites, goods, services, technologies, health, education, production, transportation, company_region, company_city, company_urls, facebook, vk, tiktok, telegram, instagram):
    return await UsersRepository().update_company(user_id, company_id, company_name, official_address, official_requisites, goods, services, technologies, health, education, production, transportation, company_region, company_city, company_urls, facebook, vk, tiktok, telegram, instagram)

async def delete_company(user_id, company_id):
    await UsersRepository().delete_company(user_id=user_id, company_id=company_id)

async def list_notifications(user_id, limit):
    return await UsersRepository().list_notifications(user_id=user_id, limit=limit)

async def add_notification(user_id, text, source):
    return await UsersRepository().add_notification(user_id=user_id, text=text, source=source)

async def delete_notification(user_id, notification_id):
    return await UsersRepository().delete_notification(user_id=user_id, notification_id=notification_id)

async def clear_notifications(user_id, limit):
    return await UsersRepository().clear_notifications(user_id=user_id, limit=limit)