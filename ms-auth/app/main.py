from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import v1_router
from app.config import logger
from app.database import MysqlManager
# from app.database.rabbit_mq import RabbitManager
from app.middlewares.auth_middleware import ApiKeyMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://193.27.228.18", "http://193.27.228.19",
                   "http://193.27.228.20", "http://dev.brendboost.ru", "http://brendboost.ru",
                   "https://dev.brendboost.ru", "https://brendboost.ru", '*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ApiKeyMiddleware)


@app.on_event("startup")
async def on_startup():
    await MysqlManager.connect()
    # await RabbitManager.connect()
    # await RedisManager.connect()
    logger.info('Startup event - connecting to the database')


app.include_router(v1_router)
