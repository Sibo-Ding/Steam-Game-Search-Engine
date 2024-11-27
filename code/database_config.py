import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
DATABASE_DATABASE = os.environ["DATABASE_DATABASE"]

ASYNCPG_DATABASE_CONFIG = {
    "user": DATABASE_USERNAME,
    "password": DATABASE_PASSWORD,
    "host": DATABASE_HOST,
    "port": DATABASE_PORT,
    "database": DATABASE_DATABASE,
}
