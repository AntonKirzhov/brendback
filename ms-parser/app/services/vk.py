
from app.enums.parsers import ParserStatus, ParserType
from app.parsers.vk.vk_groups import get_groups_data
from app.parsers.vk.vk_posts import get_posts_data
from app.schemas.parser import BaseParsersSchema
from app.services import parser


async def get_all_groups_parser(count, fields, user_id, is_user_ids, q, country_id):
    data = await get_groups_data(count, fields, is_user_ids, q, country_id)
    parser_data = BaseParsersSchema(
        parser_type=ParserType.vk_groups,
        owner_id=user_id,
        status=ParserStatus.parsed,
        parser_data=list(data)
    )
    user_parser = await parser.create_base(parser_data)
    return user_parser


async def get_all_posts_parser(count, group_screen_name, fields, user_id, comments):
    data = await get_posts_data(count, group_screen_name, fields, comments)
    parser_data = BaseParsersSchema(
        parser_type=ParserType.vk_posts,
        owner_id=user_id,
        status=ParserStatus.parsed,
        parser_data=list(data)
    )
    user_parser = await parser.create_base(parser_data)
    return user_parser
