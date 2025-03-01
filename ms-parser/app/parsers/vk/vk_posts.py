import asyncio
import datetime
from typing import List

import aiohttp

from app.schemas.vk import VKPostsParserFields
# TODO we have to separate services or rename structure
from app.config.settings import VK_ACCESS_TOKEN  # type: ignore


async def fetch_posts(session, offset, count, group_screen_name):
    payload = {
        "access_token": VK_ACCESS_TOKEN,
        "v": "5.84",
        "domain": group_screen_name,
        "count": count,
        "offset": offset,
    }

    async with session.get(
        "https://api.vk.com/method/wall.get", params=payload
    ) as response:
        data = await response.json()
        return data["response"]["items"]


async def get_all_posts(count, group_screen_name):
    all_posts = []
    offset = 0
    async with aiohttp.ClientSession() as session:
        while offset < count:
            data = await fetch_posts(session, offset, count, group_screen_name)
            all_posts.extend(data)
            offset += 100
    return all_posts

async def get_post_comments(post, comments):
    payload = {
        "access_token": VK_ACCESS_TOKEN,
        "v": "5.84",
        "count": comments,
        "owner_id": post['owner_id'],
        "post_id": post['id'],
        "sort": "desc"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.vk.com/method/wall.getComments", params=payload
        ) as response:
            data = await response.json()
            comments_text = ""
            for post_data in data["response"]["items"]:
                comments_text += f"id{post_data['from_id']} - {post_data['text']}\n"

            return comments_text

async def get_posts_data(count, group_screen_name, fields_to_parse: List[str], comments) -> list:
    get_all_data = []
    posts = await get_all_posts(count, group_screen_name)
    for post in posts:
        if str(comments) != "":
            post_comments = await get_post_comments(post, int(comments))
            await asyncio.sleep(1)
        post_data = VKPostsParserFields(
            post_id=post['id'],
            number_of_comments=post["comments"]["count"]
            if "number_of_comments" in fields_to_parse
            else None,
            post_likes=post["likes"]["count"]
            if 'post_likes' in fields_to_parse else None,
            post_text=post.get("text")
            if 'post_text' in fields_to_parse else None,
            # TODO owner id is un exist field in VKPostsParserFields
            owner_id=post["owner_id"]  # type: ignore
            if 'owner_id' in fields_to_parse else None,
            post_reposts=post.get("reposts")["count"]
            if "post_reposts" in fields_to_parse
            else None,
            post_views=post.get("views")["count"]
            if "post_views" in fields_to_parse
            else None,
            crated_at=datetime.datetime.fromtimestamp(post.get("date")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if "crated_at" in fields_to_parse
            else None,
            comments=post_comments if comments != "" else None
        )
        get_all_data.append(post_data)

    filtered_data = [
        {field: getattr(data, field) for field in fields_to_parse}
        for data in get_all_data
    ]
    return filtered_data
