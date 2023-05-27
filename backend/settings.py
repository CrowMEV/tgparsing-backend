import os

DB_NAME = os.getenv("DB_NAME")
DB_USER_NAME = os.getenv("DB_USER_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

JWT_SECRET = os.getenv("JWT_SECRET")

MANAGER_SECRET = os.getenv("MANAGER_SECRET")

DB_URL = f"postgresql+asyncpg://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL_NO_ASYNC = f"postgresql+psycopg2://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_API_URL = os.getenv("BASE_API_URL")

UPLOADED_FILES_PATH = "media/"
