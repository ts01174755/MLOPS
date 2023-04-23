import os
from dotenv import load_dotenv, find_dotenv
from src.model.mongodb import MongoDB
from src.model.postgres import PostgresDB
import pandas as pd

load_dotenv(find_dotenv("env/.env"))
pd.set_option("display.max_columns", None)

GITHUB_URL = "https://github.com/ts01174755/MLOPS.git"
CONTAINERNAME_PYTHON_3_8_18 = "python3.8.16"
CONTAINERNAME_FILE_PATH = "Users/peiyuwu/Files"
CONTAINERNAME_ROOT_PATH_DOCKER = "/Users/peiyuwu/MLOPS"
CONTAINERNAME_ROOT_PATH_LOCAL = "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS"
CONTAINER_INTERPRETER = "python3.8"
MONGODB_DOCKER = MongoDB(
    user_name=os.getenv("MongoDB_USER"),
    user_password=os.getenv("MongoDB_PASSWORD"),
    port=int(os.getenv("MongoDB_PORT")),
    host="mongodb",
    database_name="originaldb",
)
MONGODB_LOCAL = MongoDB(
    user_name=os.getenv("MongoDB_USER"),
    user_password=os.getenv("MongoDB_PASSWORD"),
    port=int(os.getenv("MongoDB_PORT")),
    host=os.getenv("MongoDB_HOST"),
    database_name="originaldb",
)
POSTGRESDB_DOCKER = PostgresDB(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="postgres15.2",  # route 在 Docker 部署的Host
    port=os.getenv("POSTGRES_PORT"),
    database="originaldb",
)
POSTGRESDB_LOCAL = PostgresDB(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database="originaldb",
)
