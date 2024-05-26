from datetime import datetime
from typing import Optional
import json
from fastapi import HTTPException

from app.database.mysql import MysqlManager
from app.repositories.user_parsers import UserParsersRepository

async def get_user_by_id(user_id: str):
    await MysqlManager.db.ping()
    query = await MysqlManager.cursor.execute(f"SELECT `_id`, `selected_company` FROM `users` WHERE `_id` = '{user_id}'")
    result = await MysqlManager.cursor.fetchall()
    return result[0]

async def create_base(parser) -> dict:
    if type(parser) != dict:
        parser = parser.dict()
    await MysqlManager.db.ping()
    user = await get_user_by_id(parser['owner_id'])
    await MysqlManager.cursor.execute(f"INSERT INTO `parsers` (`company`, `parser_type`, `owner_id`, `status`, `parser_data`) VALUES ('{user['selected_company']}', '{parser['parser_type']}', '{parser['owner_id']}', '{parser['status']}', %s)", [json.dumps(parser['parser_data']).replace("'", '\\"')])
    await MysqlManager.db.commit()
    query = await MysqlManager.cursor.execute(f"SELECT * FROM `parsers` WHERE `_id` = '{MysqlManager.cursor.lastrowid}'")
    result = await MysqlManager.cursor.fetchall()
    return result[0]

async def delete_parser_by_type(parser_type: str, owner_id: str, from_created_at: Optional[datetime],
                                to_created_at: Optional[datetime]) -> list:
    parser = await UserParsersRepository().delet_by_type(parser_type=parser_type, owner_id=owner_id,
                                                         from_created_at=from_created_at,
                                                         to_created_at=to_created_at)
    if not parser:
        raise HTTPException(status_code=404, detail='There are no chosen database with this type')
    return parser


async def get_parser_by_id(parser_id: str, owner_id: str) -> dict:
    await MysqlManager.db.ping()
    query = await MysqlManager.cursor.execute(f"SELECT * FROM `parsers` WHERE `_id` = '{parser_id}' AND `owner_id` = '{owner_id}'")
    result = await MysqlManager.cursor.fetchall()
    if len(result) <= 0:
        raise HTTPException(status_code=404, detail='There are no chosen database with this id')
    else:
        result[0]['parser_data'] = json.loads(result[0]['parser_data'])
        return result[0]

async def get_parsers_by_user(user_id: str):
    await MysqlManager.db.ping()
    user = await get_user_by_id(user_id);
    query = await MysqlManager.cursor.execute(f"SELECT * FROM `parsers` WHERE `owner_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
    result = await MysqlManager.cursor.fetchall()
    return result


async def get_all():
    return await UserParsersRepository().get_all()


async def get_all_by_base(base: str):
    return await UserParsersRepository().get_all_by_type(base)


async def get_all_by_status(status: str):
    return await UserParsersRepository().get_all_by_status(status)


async def delete_by_id(parser_id: str, owner_id: str):
    parser_id = parser_id.replace("parser_id=","")
    await MysqlManager.db.ping()
    await MysqlManager.cursor.execute(f"DELETE FROM `parsers` WHERE `_id` = '{parser_id}'")
    await MysqlManager.db.commit()

async def delete_all(parser_ids, owner_id: str):
    if not parser_ids:
        raise HTTPException(status_code=400, detail="No parser IDs provided")
    parser_ids = [str(i) for i in parser_ids]
    await MysqlManager.db.ping()
    await MysqlManager.cursor.execute(f"DELETE FROM `parsers` WHERE `owner_id` = '{owner_id}' AND (`_id`) IN ({','.join(parser_ids)})")
    await MysqlManager.db.commit()

async def delete_all_data(owner_id: str):
    if not owner_id:
        raise HTTPException(status_code=400, detail="No user ID provided")

    deleted_count = await UserParsersRepository().delete_by_owner_id(owner_id)
    if deleted_count > 0:
        return {"deleted_count": f"Successfully deleted {deleted_count} parser(s)"}
    else:
        raise HTTPException(
            status_code=404, detail="No parsers found for deletion")
