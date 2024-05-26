import logging
import os

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s: %(message)s')


# FastAPI configuration
HOST = os.environ.get('FASTAPI_HOST', '0.0.0.0')
PORT = os.environ.get('FASTAPI_PORT', '8000')

# MongoManager configuration
MONGO_URI = "mongodb+srv://mongo:G6goEw0stB9XsF18@breanboostauth.4yhe2eg.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "branboost_auth"

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "startsback"
MYSQL_PORT = 3306

SERVICE_URL = "http://193.27.228.20:8001/api/v1"
PARSER_COLLECTION_NAME = "‘parsers’"


# Token configuration
SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TTL = 3600
JWT_REFRESH_TTL = 10000
REFRESH_TOKEN_JWT_SUBJECT: str = 'refresh'
ACCESS_TOKEN_JWT_SUBJECT: str = 'access'
TOKEN_TYPE: str = "Bearer"

# Redis configuration
REDIS_HOST: str = "redis"
REDIS_PORT: str = "6379"
REDIS_URI: str = f'redis://{REDIS_HOST}:{REDIS_PORT}'
# REDIS_URI = f'0.0.0.0:{REDIS_PORT}'

# Email configuration
EMAIL_HOST_USER: str = "ben300300@gmail.com"
EMAIL_HOST_PASSWORD: str = "pptjlyinssyxyzkf"
EMAIL_HOST: str = "smtp.gmail.com"

# Fns api
API_FNS_KEY: str = "6449c575e9a0b6f060003a8789764ad84ae02ffd"

# Test
USER_EMAIL: str = os.environ.get("USER_EMAIL", 'some_mail@mail.ru')
USER_INN: str = os.environ.get("USER_INN", '123123')

# Rabbit
RABBIT_PORT = os.environ.get("RABBIT_PORT", 5672)
RABBIT_HOST = os.environ.get("RABBIT_HOST", 'localhost')
