import asyncio
import aiomysql
from app.config import settings, logger

class MysqlManager:
    db = None
    cursor = None

    @classmethod
    async def connect(cls):
        try:
            logger.info("Connected to database.")
            cls.db = await aiomysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, user=settings.MYSQL_USER, password=settings.MYSQL_PASSWORD, db=settings.MYSQL_DATABASE, autocommit=True)
            cls.cursor = await cls.db.cursor(aiomysql.DictCursor)
            await cls.cursor.execute('SET GLOBAL max_allowed_packet=67108864;')
            await cls.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;")
        except Exception as e:
            logger.info(f"Error connecting: {str(e)}")

    @classmethod
    async def close(cls):
        if cls.db:
            await cls.cursor.close()
            cls.db.close()

    '''@classmethod
    async def get_db(cls) -> AsyncIOMotorDatabase:
        return cls.db if cls.db is not None else await cls.connect()'''