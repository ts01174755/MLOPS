import os
from dotenv import load_dotenv, find_dotenv
from src.model.mongodb import MongoDB
from src.model.postgres import PostgresDB
import pandas as pd

load_dotenv(find_dotenv("env/.env"))
pd.set_option("display.max_columns", None)

####################################################################################################################
IMAGE_PYTHON_3_8_18_TAG = "python:3.8.16"
CONTAINER_PYTHON_3_8_18_NAME = "python3.8.16"
CONTAINER_PYTHON_3_8_18_PORT_LIST = [f'{port}:{port}' for port in range(8000, 8010)]
CONTAINER_PYTHON_3_8_18_INTERPRETER = "python3.8"
CONTAINER_PYTHON_3_8_18_ROOT = "/Users/peiyuwu"
CONTAINER_PYTHON_3_8_18_ROOT_MAP = "/Users/peiyuwu/Development/docker/python3.8.16"
CONTAINER_PYTHON_3_8_18_FILE_PATH = "Users/peiyuwu/Files"
CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH = "Users/peiyuwu/Downloads"

####################################################################################################################
IMAGE_MONGODB_TAG = "mongo:5.0.15"
CONTAINER_MONGODB_NAME = "mongodb"
CONTAINER_MONGODB_PORT_LIST = ['27017:27017']
CONTAINER_MONGODB_ROOT = "/Users/peiyuwu"
CONTAINER_MONGODB_ROOT_MAP = "/Users/peiyuwu/Development/docker/mongodb"
CONTAINER_MONGO_POSTGRES_NET = "mongo-postgres-net"
CONTAINER_MONGO_ENV_DICT = {
    'MONGO_INITDB_ROOT_USERNAME': 'mongodb',
    'MONGO_INITDB_ROOT_PASSWORD': 'mongodb'
}

####################################################################################################################
IMAGE_MONGODB_EXPRESS_TAG = "mongo-express:0.54.0"
CONTAINER_MONGODB_EXPRESS_NAME = "mongo_express"
CONTAINER_MONGODB_EXPRESS_PORT_LIST = ['8081:8081']
CONTAINER_MONGODB_EXPRESS_ROOT = "/Users/peiyuwu"
CONTAINER_MONGODB_EXPRESS_ROOT_MAP = "/Users/peiyuwu/Development/docker/mongo_express"
CONTAINER_MONGO_EXPRESS_ENV_DICT = {
    'ME_CONFIG_MONGODB_SERVER': CONTAINER_MONGODB_NAME,
    'ME_CONFIG_MONGODB_ADMINUSERNAME': 'mongodb',
    'ME_CONFIG_MONGODB_ADMINPASSWORD': 'mongodb',
    'ME_CONFIG_BASICAUTH_USERNAME': 'mongoUser',
    'ME_CONFIG_BASICAUTH_PASSWORD': 'mongoUserPassword'
}

####################################################################################################################
IMAGE_POSTGRES_TAG = "postgres:15.2"
CONTAINER_POSTGRES_NAME = "postgres15.2"
CONTAINER_POSTGRES_PORT_LIST = ['5432:5432']
CONTAINER_POSTGRES_ROOT = "/Users/peiyuwu"
CONTAINER_POSTGRES_ROOT_MAP = "/Users/peiyuwu/Development/docker/postgres15.2"
CONTAINER_POSTGRES_ENV_DICT = {
    'POSTGRES_USER': 'postgres',
    'POSTGRES_PASSWORD': 'postgres',
    'POSTGRES_DB': 'postgres'
}
CONTAINER_POSTGRES_DB1 = "originaldb"

####################################################################################################################
IMAGE_PGADMIN_TAG = "dpage/pgadmin4:6.20"
CONTAINER_PGADMIN_NAME = "pgadmin4"
CONTAINER_PGADMIN_PORT_LIST = ['5050:80']
CONTAINER_PGADMIN_ROOT = "/Users/peiyuwu"
CONTAINER_PGADMIN_ROOT_MAP = "/Users/peiyuwu/Development/docker/pgadmin4"
CONTAINER_PGADMIN_ENV_DICT = {
    'PGADMIN_DEFAULT_EMAIL': 'pgadmin4@gmail.com',
    'PGADMIN_DEFAULT_PASSWORD': 'pgadmin4'
}

####################################################################################################################
MLOPS_ROOT_PATH_DOCKER = "/Users/peiyuwu/MLOPS"
MLOPS_ROOP_PATH_LOCAL = "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS"
GITHUB_URL = "https://github.com/ts01174755/MLOPS.git"

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
