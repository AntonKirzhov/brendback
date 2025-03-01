import typing as tp
from random import randint
from datetime import datetime
import json

from fastapi import APIRouter, Request


from app.config import logger  # noqa
from app.enums import UserRole
from app.schemas import (
    BaseUserRead as BaseUserReadSchema,
    LegalUserCreateUpdate as CreateUpdateRegularUserSchema,
    PrivateUserCreateUpdate as CreateUpdatePrivateUserSchema,
    RefreshToken as RefreshTokenSchema,
    Login as LoginSchema,
    Token as TokenSchema,
    Email as EmailSchema,
    ResetPasswords as ResetPasswordsSchema,
    RetrieveLogin as RetrieveLoginSchema,
    PrivateUserCreate,
    LegalUserCreate,
)
from app.schemas.tokens import ObtainTokenResponseSchema
from app.schemas.users import PatchUserUpdateRequest, ReadUserProjects
from app import services

user_routes = APIRouter()


@user_routes.get("/get_projects/", status_code=200, response_model=ReadUserProjects)
async def get_user_projects(request: Request):
    user_id = request.state.user_id
    return await services.get_user_by_id(user_id)


@user_routes.get("/me/", status_code=200)
async def get_user(request: Request):
    return await services.get_user_by_id(user_id=request.state.user_id)


@user_routes.delete("/me/", status_code=200)
async def delete_person(request: Request):
    return await services.delete_person(user_id=request.state.user_id)


@user_routes.patch("/me/", status_code=200, response_model=BaseUserReadSchema)
async def update_user_me(request: Request, body: PatchUserUpdateRequest):
    return await services.update_user(user_id=request.state.user_id, instance=body)


@user_routes.post("/private_person/register/", status_code=201, response_model=ObtainTokenResponseSchema)
async def register_private_person(data: PrivateUserCreate) -> tp.Dict[str, tp.Any]:
    person = CreateUpdatePrivateUserSchema(
        role=UserRole.PRIVATE_PERSON,
        is_verified=False,
        created_at=datetime.now(), **data.dict()
    )
    user = await services.create_user(person=person)
    tokens = await services.create_tokens(user_id=str(user.get("_id")))
    return tokens.dict()
    #return 404

@user_routes.post("/legal_person/register/", status_code=201, response_model=TokenSchema)
async def register_legal_person(data: LegalUserCreate):
    person = CreateUpdatePrivateUserSchema(
        role=UserRole.LEGAL_PERSON,
        is_verified=False,
        created_at=datetime.now(), **data.dict()
    )
    user = await services.create_user(person=person)
    tokens = await services.create_tokens(user_id=str(user.get("_id")))
    return tokens.dict()


@user_routes.post("/login/", response_model=RetrieveLoginSchema, status_code=200)
async def login(data: LoginSchema):
    return await services.login_user(data=data)


@user_routes.post("/forgot_password/", status_code=200)
async def forgot_password(email: EmailSchema):
    await services.forgot_password(email=email)


@user_routes.post("/reset_password/", status_code=200)
async def reset_password(data: ResetPasswordsSchema):
    return await services.reset_password(data=data)


@user_routes.post("/activate/", status_code=200)
async def activate_person(user_id: str, code: str):
    # todo: activate person in registration and add restrictions for unferifed user
    status = await services.activate_person(user_id=user_id, code=code)
    return status

@user_routes.post("/select_company/", status_code=200)
async def select_company(user_id: str, company_id: str):
    # todo: activate person in registration and add restrictions for unferifed user
    result = await services.select_company(user_id=user_id, company_id=company_id)
    return result

@user_routes.post("/refresh_token/", response_model=TokenSchema, status_code=200)
async def refresh_token(token: RefreshTokenSchema):
    return await services.generate_access_token_from_refresh(refresh_token=token.refresh_token)


@user_routes.post("/check_inn/", status_code=200)
async def check_company_by_inn(inn: str):
    result = await services.check_exist_company_by_inn(inn)
    return result

@user_routes.post("/check_inn_local/", status_code=200)
async def check_company_by_inn(inn: str):
    rand = randint(0, 1)
    fname = ""
    if rand == 0:
        fname = "response_1711114078474.json"
    elif rand == 1:
        fname = "response_1711114090913.json"

    file = open(fname, "r")
    text = file.read()
    file.close()

    return json.loads(text)

@user_routes.post("/update_tariff/", status_code=200)
async def update_tariff(user_id: str, tariff: str):
    status = await services.update_tariff(user_id=user_id, tariff=tariff)
    return status

@user_routes.post("/new_ticket/", status_code=200)
async def new_ticket(user_id: str, text: str):
    status = await services.new_ticket(user_id=user_id, text=text)
    return status
