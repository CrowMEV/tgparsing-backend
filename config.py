import os
from dotenv import load_dotenv


load_dotenv()


BD_NAME = os.getenv('BD_NAME')
BD_USER_NAME = os.getenv('BD_USER_NAME')
BD_PASSWORD = os.getenv('BD_PASSWORD')
BD_HOST = os.getenv('BD_HOST')
BD_PORT = os.getenv('BD_PORT')

JWT_SECRET = os.getenv('JWT_SECRET')

MANAGER_SECRET = os.getenv('MANAGER_SECRET')

DB_URL = f'postgresql+asyncpg://{BD_USER_NAME}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}/{BD_NAME}'
DB_URL_NO_ASYNC = f'postgresql+psycopg2://{BD_USER_NAME}:{BD_PASSWORD}@{BD_HOST}:{BD_PORT}/{BD_NAME}'

BASE_API_URL = os.getenv('BASE_API_URL')

UPLOADED_FILES_PATH = 'media/'
