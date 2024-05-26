import asyncio
from typing import List

import aiohttp

# TODO we have to separate services or rename structure
from app.config.settings import VK_ACCESS_TOKEN, logger  # type: ignore
from app.schemas.vk import VKGroupsParserFields

payload = {
    "access_token": VK_ACCESS_TOKEN,
    "v": "5.81",
}


async def fetch_groups(session, count, offset, q, country_id=None):
    payload["count"] = count
    payload["offset"] = offset
    payload["q"] = q
    payload["sort"] = 0
    if country_id != None:
        payload["country_id"] = country_id

    async with session.get(
        "https://api.vk.com/method/groups.search", params=payload
    ) as response:
        data = await response.json()
        print(data)
        return data["response"]["items"]

async def fetch_members(session, group_id, count):
    payload["sort"] = "id_desc"
    members = []
    offsets = 0
    if count > 1000:
        print(1)
        offsets = int(count/1000)
        print(offsets)
    current_offset = 0
    if offsets > 0:
        while current_offset-1 != offsets:
            print(f"CURR {current_offset}")
            if current_offset == offsets:
                payload["count"] = count-(1000*current_offset)
                print(f"count-{count-(1000*current_offset)}")
            else:
                payload["count"] = 1000
            payload["offset"] = 1000*current_offset
            print(f"PAYLOAD {1000*current_offset}")
            async with session.get(
                "https://api.vk.com/method/groups.getMembers", params=payload
            ) as response:
                data = await response.json()
                for item in data["response"]["items"]:
                    members.append(str(item['id']))

                current_offset += 1
                await asyncio.sleep(5)

    elif offsets == 0:
        payload["count"] = count
        payload["offset"] = 0
        async with session.get(
            "https://api.vk.com/method/groups.getMembers", params=payload
        ) as response:
            data = await response.json()
            for item in data["response"]["items"]:
                members.append(str(item['id']))
    return ','.join(members)

async def get_all_groups(count, is_user_ids, q, country_id):
    offset = 0
    all_groups = []
    async with aiohttp.ClientSession() as session:
        while offset < count:
            data = await fetch_groups(session, count, offset, q, country_id)
            for group in data:
                payload["group_id"] = group['id']
                payload[
                    "fields"
                ] = "status, members_count, description, country, counters, contacts"
                async with session.get(
                    "https://api.vk.com/method/groups.getById", params=payload
                ) as response:
                    await asyncio.sleep(1)
                    groups_data = await response.json()
                    if str(is_user_ids) != "false" and str(is_user_ids) != "False":
                        groups_data["response"][0]["members_ids"] = await fetch_members(session, groups_data["response"][0]['id'], int(is_user_ids))
                    all_groups.append(groups_data["response"][0])
            offset += 100
    return all_groups


async def get_item(item: str, group, sub_item=None):
    try:
        elem = group[item]
        if sub_item is not None and isinstance(elem, dict) and sub_item in elem:
            return elem[sub_item]
        else:
            return "Элемент отсутствует" if elem is None else elem
    except Exception as ex:
        return "Элемент отсутствует"

async def build_contacts(contacts):
    contacts_text = ""
    for contact in contacts:
        if 'desc' in contact:
            if 'user_id' in contact:
                contacts_text += f"id{contact['user_id']} - {contact['desc']}\n"
            elif 'email' in contact:
                contacts_text += f"{contact['email']} - {contact['desc']}\n"
        else:
            if 'user_id' in contact:
                contacts_text += f"id{contact['user_id']}\n"
            elif 'email' in contact:
                contacts_text += f"{contact['email']}\n"

    return contacts_text

async def get_groups_data(count, fields_to_parse: List[str], is_user_ids, q, country_id) -> list:
    get_all_data = []
    groups = await get_all_groups(count, is_user_ids, q, country_id)
    for group in groups:
        if 'contacts' in group:
            group_contacts = await build_contacts(group['contacts'])
        else:
            group_contacts = None
        post_data = VKGroupsParserFields(
            id=await get_item("id", group) if "id" in fields_to_parse else None,
            group_description=await get_item("description", group),
            group_screen_name=await get_item("name", group),
            members_count=await get_item("members_count", group),
            group_articles_number=await get_item("counters", group, "articles"),
            group_videos_number=await get_item("counters", group, "videos"),
            group_country=await get_item("country", group, "title"),
            group_contacts=await get_item("contacts", group),
            members_ids=await get_item("members_ids", group) if is_user_ids else None,
            contacts=group_contacts,
        )
        get_all_data.append(post_data)
    filtered_data = [
        {field: getattr(data, field) for field in fields_to_parse}
        for data in get_all_data
    ]
    return filtered_data
