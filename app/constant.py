from os import getenv


DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_PORT = getenv("DB_PORT")
DB_TABLE = getenv("DB_TABLE")
DB_USER = getenv("DB_USER")

DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_TABLE}"
