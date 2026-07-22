import os

import pymysql

from dotenv import load_dotenv
from app.utils.path_manager import PathManager

RUTA_ENV = PathManager.get_env_path()
load_dotenv(RUTA_ENV)


def get_connection():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if not db_host:
        raise ValueError("Falta variable de entorno: DB_HOST")
    if not db_port:
        raise ValueError("Falta variable de entorno: DB_PORT")
    if not db_user:
        raise ValueError("Falta variable de entorno: DB_USER")
    if not db_password:
        raise ValueError("Falta variable de entorno: DB_PASSWORD")
    if not db_name:
        raise ValueError("Falta variable de entorno: DB_NAME")

    return pymysql.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_password,
        database=db_name,
        charset="utf8mb4"
    )
