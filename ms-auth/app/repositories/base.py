import aiohttp
import json
import typing as tp
from typing import List

from bson import ObjectId

from app.database import MysqlManager
from app.schemas import BaseUserRead

tariff_json = {
    "name": "Не выбран",
    "voice_mailing": False,
    "parsers": False,
    "text_mailing": False,
    "ai": False,
    "advertising": False,
    "marketplaces": False,
    "reports": False
}

class BaseRepository(MysqlManager):
    collection: str

    def __init__(self):
        super().__init__()

    async def get_by_id(self, _id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `users` WHERE `_id` = '{_id}'")
        result = await self.cursor.fetchall()
        return result[0]

    async def update_password(self, user_id: str, _password: str):
        return await self.db[self.collection].update_one({'_id': user_id}, {'_password': _password})

    async def get_by_email(self, email: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `users` WHERE `email` = '{email}'")
        result = await self.cursor.fetchall()
        return result

    async def get_by_name(self, name: str):
        return await self.db[self.collection].find_one({"name": name})

    async def get_all(self) -> List[BaseUserRead]:
        await self.get_db()
        return await self.db[self.collection].find().to_list(length=None)

    async def create(self, instance: dict) -> dict:
        await self.db.ping()
        print(instance)
        await self.cursor.execute(f"INSERT INTO `users` (`role`, `email`, `password`, `last_name`, `first_name`, `phone`, `tariff`) VALUES ('{instance['role']}', '{instance['email']}', '{instance['password']}', '{instance['additional_info']['last_name']}', '{instance['additional_info']['first_name']}', '{instance['phone']}', %s)", [json.dumps(tariff_json).replace("'", '\\"')])
        await self.db.commit()
        query = await self.cursor.execute(f"SELECT * FROM `users` WHERE `_id` = '{self.cursor.lastrowid}'")
        result = await self.cursor.fetchall()
        return result[0]

    async def create_legal(self, instance: dict) -> dict:
        await self.db.ping()
        print(instance)
        await self.cursor.execute(f"INSERT INTO `users` (`role`, `email`, `password`, `last_name`, `first_name`, `phone`, `inn`, `company_name`, `tariff`) VALUES ('{instance['role']}', '{instance['email']}', '{instance['password']}', '{instance['additional_info']['last_name']}', '{instance['additional_info']['first_name']}', '{instance['phone']}', '{instance['additional_info']['inn']}', '{instance['additional_info']['company_name']}', %s)", [json.dumps(tariff_json).replace("'", '\\"')])
        await self.db.commit()
        query = await self.cursor.execute(f"SELECT * FROM `users` WHERE `_id` = '{self.cursor.lastrowid}'")
        result = await self.cursor.fetchall()
        return result[0]

    async def get_user_company_by_id(self, company_id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT `company_id`, `user_id` FROM `companies` WHERE `company_id` = '{company_id}'")
        result = await self.cursor.fetchall()
        return result

    async def change_company_by_id(self, _id: str, company_id: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `selected_company` = '{company_id}' WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def update_by_id(self, _id: str, data):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `email` = '{data['email']}', `phone` = '{data['phone']}', `first_name` = '{data['first_name']}', `last_name` = '{data['last_name']}' WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def update_user_password(self, _id: str, password: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `password` = '{password}' WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def update_user_avatar_link(self, _id: str, avatar_link: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `avatar_link` = '{avatar_link}' WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def update_email_code(self, email: str, code: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `email_code` = '{code}' WHERE `email` = '{email}'")
        await self.db.commit()

    async def update_tariff(self, _id: str, tariff: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `tariff` = '{tariff}' WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def activate_user(self, _id: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `users` SET `is_verified` = 'True' WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def delete_by_id(self, _id: str):
        await self.db.ping()
        await self.cursor.execute(f"DELETE FROM `users` WHERE `_id` = '{_id}'")
        await self.db.commit()

    async def get_user_by_id(self, user_id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT `_id`, `selected_company` FROM `users` WHERE `_id` = '{user_id}'")
        result = await self.cursor.fetchall()
        return result[0]

    async def list_audioclips(self, user_id: str):
        user = await self.get_user_by_id(user_id=user_id)
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `audioclips` WHERE `user_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
        result = await self.cursor.fetchall()
        return result

    async def create_audioclip(self, user_id: str, clip_name: str, clip_description: str, zvonok_id: str):
        user = await self.get_user_by_id(user_id=user_id)
        await self.db.ping()
        await self.cursor.execute(f"INSERT INTO `audioclips` (`user_id`, `company`, `zvonok_id`, `clip_name`, `clip_description`) VALUES ('{user_id}', '{user['selected_company']}', '{zvonok_id}', '{clip_name}', '{clip_description}')")
        await self.db.commit()

        return self.cursor.lastrowid

    async def delete_audioclip(self, user_id: str, clip_id: str):
        await self.db.ping()
        await self.cursor.execute(f"DELETE FROM `audioclips` WHERE `user_id` = '{user_id}' AND `audioclip_id` = '{clip_id}'")
        await self.db.commit()

    async def list_calls(self, user_id: str):
        user = await self.get_user_by_id(user_id=user_id)
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `calls` WHERE `user_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
        result = await self.cursor.fetchall()
        return result

    async def get_audioclip_by_audio(self, _id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `audioclips` WHERE `audioclip_id` = '{_id}'")
        result = await self.cursor.fetchone()
        return result['zvonok_id']

    async def create_call(self, user_id: str, call_name: str, audioclip_id: str, phones: list[str]):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://zvonok.com/manager/cabapi_external/api/v1/audio/info/?public_key=46680aa2d0a4979f45aed876d3bf2f1f&audioclip_id={audioclip_id}") as response:
                text = await response.text()
                text = json.loads(text)
                price = 0.05*len(phones)*int(text['audioclip']['length_val'])
                user = await self.get_user_by_id(user_id=user_id)
                await self.db.ping()
                await self.cursor.execute(f"INSERT INTO `calls` (`user_id`, `company`, `name`, `audioclip_id`, `phones`, `price`) VALUES ('{user_id}', '{user['selected_company']}', '{call_name}', '{audioclip_id}', '{','.join(phones)}', '{price}')")
                await self.db.commit()

    async def delete_call(self, user_id: str, call_id: str):
        await self.db.ping()
        await self.cursor.execute(f"DELETE FROM `calls` WHERE `user_id` = '{user_id}' AND `call_id` = '{call_id}'")
        await self.db.commit()

    async def list_main_companies(self, user_id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT `company_id`, `company_name` FROM `companies` WHERE `user_id` = '{user_id}' ORDER BY `company_id` DESC LIMIT 3")
        result = await self.cursor.fetchall()
        return result

    async def list_companies(self, user_id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `companies` WHERE `user_id` = '{user_id}'")
        result = await self.cursor.fetchall()
        return result

    async def get_selected_company_by_user_id(self, user_id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT `_id`, `selected_company` FROM `users` WHERE `_id` = '{user_id}'")
        result = await self.cursor.fetchone()
        company_id = result['selected_company']
        if company_id == "-":
            return "Не выбрана"
        else:
            query = await self.cursor.execute(f"SELECT * FROM `companies` WHERE `user_id` = '{user_id}' AND `company_id` = '{company_id}'")
            result = await self.cursor.fetchone()
            return result

    async def get_company_by_id(self, user_id: str, company_id: str):
        await self.db.ping()
        query = await self.cursor.execute(f"SELECT * FROM `companies` WHERE `user_id` = '{user_id}' AND `company_id` = '{company_id}'")
        result = await self.cursor.fetchone()
        return result

    async def create_company(self, user_id: str, company_name: str, official_address: str, official_requisites: str, goods: str, services: str, technologies: str, health: str, education: str, production: str, transportation: str, company_region: str, company_city: str, company_urls: str, facebook: str, vk: str, tiktok: str, telegram: str, instagram: str):
        await self.db.ping()
        await self.cursor.execute(f"INSERT INTO `companies` (`user_id`, `company_name`, `official_address`, `official_requisites`, `goods`, `services`, `technologies`, `health`, `education`, `production`, `transportation`, `company_region`, `company_city`, `company_urls`, `facebook`, `vk`, `tiktok`, `telegram`, `instagram`) VALUES ('{user_id}', '{company_name}', '{official_address}', '{official_requisites}', '{goods}', '{services}', '{technologies}', '{health}', '{education}', '{production}', '{transportation}', '{company_region}', '{company_city}', '{company_urls}', '{facebook}', '{vk}', '{tiktok}', '{telegram}', '{instagram}')")
        await self.db.commit()

    async def update_company(self, user_id: str, company_id: str, company_name: str, official_address: str, official_requisites: str, goods: str, services: str, technologies: str, health: str, education: str, production: str, transportation: str, company_region: str, company_city: str, company_urls: str, facebook: str, vk: str, tiktok: str, telegram: str, instagram: str):
        await self.db.ping()
        await self.cursor.execute(f"UPDATE `companies` SET `company_name` = '{company_name}', `official_address` = '{official_address}', `official_requisites` = '{official_requisites}', `goods` = '{goods}', `services` = '{services}', `technologies` = '{technologies}', `health` = '{health}', `education` = '{education}', `production` = '{production}', `transportation` = '{transportation}', `company_region` = '{company_region}', `company_city` = '{company_city}', `company_urls` = '{company_urls}', `facebook` = '{facebook}', `vk` = '{vk}', `tiktok` = '{tiktok}', `telegram` = '{telegram}', `instagram` = '{instagram}' WHERE `user_id` = '{user_id}' AND `company_id` = '{company_id}'")
        await self.db.commit()

    async def delete_company(self, user_id: str, company_id: str):
        await self.db.ping()
        await self.cursor.execute(f"DELETE FROM `companies` WHERE `user_id` = '{user_id}' AND `company_id` = '{company_id}'")
        await self.db.commit()

    async def list_notifications(self, user_id: str, limit: int):
        await self.db.ping()
        if limit <= 0:
            query = await self.cursor.execute(f"SELECT * FROM `notifications` WHERE `user_id` = '{user_id}' ORDER BY `notification_id` DESC")
        elif limit > 0:
            query = await self.cursor.execute(f"SELECT * FROM `notifications` WHERE `user_id` = '{user_id}' ORDER BY `notification_id` DESC LIMIT {str(limit)}")
        result = await self.cursor.fetchall()
        return result

    async def add_notification(self, user_id: str, text: str, source: str):
        await self.db.ping()
        await self.cursor.execute(f"INSERT INTO `notifications` (`user_id`, `text`, `source`) VALUES ('{user_id}', '{text}', '{source}')")
        await self.db.commit()

    async def delete_notification(self, user_id: str, notification_id: str):
        await self.db.ping()
        await self.cursor.execute(f"DELETE FROM `notifications` WHERE `user_id` = '{user_id}' AND `notification_id` = '{notification_id}'")
        await self.db.commit()

    async def clear_notifications(self, user_id: str, limit: int):
        await self.db.ping()
        if limit <= 0:
            await self.cursor.execute(f"DELETE FROM `notifications` WHERE `user_id` = '{user_id}' ORDER BY `notification_id` DESC")
        elif limit > 0:
            await self.cursor.execute(f"DELETE FROM `notifications` WHERE `user_id` = '{user_id}' ORDER BY `notification_id` DESC LIMIT {str(limit)}")
        await self.db.commit()

    # bulk create; bulk update, bulk_delete
