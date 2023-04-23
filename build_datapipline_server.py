import os
import sys
import env_config
from PostgresDB.controller.postgres_parse_mongodb_data import PosgresParseMongodbData
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from src.model.docker_cmd import DockerCmd

# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8002
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# ------------------------ env_params ------------------------
CONTAINER_NAME = env_config.CONTAINERNAME_PYTHON_3_8_18     # 執行環境
FILE_PATH_DOCKER  = env_config.CONTAINERNAME_FILE_PATH      # 存放資料的位置
ROOT_PATH_DOCKER = env_config.CONTAINERNAME_ROOT_PATH_DOCKER    # DOCKER 執行路徑
ROOT_PATH_LOCAL = env_config.CONTAINERNAME_ROOT_PATH_LOCAL      # LOCAL 執行路徑
INTERPRETER = env_config.CONTAINER_INTERPRETER      # 執行的python解釋器
ROUTE_NAME = f"{ROOT_PATH_DOCKER}/build_datapipline_server.py"    # 執行的程式
POSTGRESDB = env_config.POSTGRESDB_DOCKER # postgres連線資訊
# POSTGRESDB = env_config.POSTGRESDB_LOCAL # postgres連線資訊
MONGODB = env_config.MONGODB_DOCKER     # mongodb連線資訊
# MONGODB = env_config.MONGODB_LOCAL    # mongodb連線資訊
DEPLOY_DETACH = False

# ------------------------- ROUTE ----------------------------
app = FastAPI()


class STCrawlerRequestBody(BaseModel):
    DATA_TIME: str = None
    MONGODB_COLLECTION: str = None
    MONGODB_QUERY: dict = None
    PROGRESDB_TABLE: str = None
    PROGRESDB_SCHEMA: dict = None
    PROGRESDB_SCHEMA_DICT: dict = None
    KWARGS: dict = None

# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.post("/PostgresDB/mongodbToProgres/stCreateCourseForm")
def st_create_course_form(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    # 每日執行 - 爬蟲
    posgresParseMongodbData = PosgresParseMongodbData()
    googleFormDF = posgresParseMongodbData.parseGoogleSTFromData(
        MONGODB=MONGODB,
        DATA_TIME=params.DATA_TIME,
        MONGODB_COLLECTION=params.MONGODB_COLLECTION,
        MONGODB_QUERY=params.MONGODB_QUERY,
        PROGRESDB_SCHEMA_DICT=params.PROGRESDB_SCHEMA_DICT,
    )

    # 連接PostgresDB與寫入資料
    posgresParseMongodbData.insertPostgresData(
        PROGRESDB=POSTGRESDB,
        PROGRESDB_TABLE=params.PROGRESDB_TABLE,
        PROGRESDB_SCHEMA=params.PROGRESDB_SCHEMA,
        dataFrame=googleFormDF,
    )
    return {"message": "insert success"}


@app.post("/PostgresDB/mongodbToProgres/stAdminCourses")
def st_admin_course(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    # 每日執行 - 爬蟲
    posgresParseMongodbData = PosgresParseMongodbData()
    googleFormDF = posgresParseMongodbData.parseSTData(
        MONGODB=MONGODB,
        MONGODB_COLLECTION=params.MONGODB_COLLECTION,
        MONGODB_QUERY=params.MONGODB_QUERY,
        PROGRESDB_SCHEMA_DICT=params.PROGRESDB_SCHEMA_DICT,
        DATA_TIME=params.DATA_TIME,
    )

    # 連接PostgresDB與寫入資料
    posgresParseMongodbData.insertPostgresData(
        PROGRESDB=POSTGRESDB,
        dataFrame=googleFormDF,
        PROGRESDB_TABLE=params.PROGRESDB_TABLE,
        PROGRESDB_SCHEMA=params.PROGRESDB_SCHEMA,
    )
    return {"message": "insert success"}

@app.post("/PostgresDB/mongodbToProgres/makeSchemaFile")
def make_schema_file(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    posgresParseMongodbData = PosgresParseMongodbData()
    posgresParseMongodbData.makeDataSchema(
        PROGRESDB=POSTGRESDB,
        tableName=params.PROGRESDB_TABLE,
        schemaDict=params.KWARGS['PROGRESDB_SCHEMA_DICT'],
        columnList=params.KWARGS['COLUMNS_LIST'],
        schemaFilePath=f'{FILE_PATH_DOCKER}/{params.KWARGS["PROGRESDB_SCHEMA_FILE"]}.csv',
    )
    return {"message": "insert success"}


# Main entry point
if __name__ == "__main__":
    # 執行環境 - 基本上不需要動
    if RUN == "docker":
        # 移除container中的舊程式
        DockerCmd.dockerExec(
            name=CONTAINER_NAME,
            cmd=f"rm -rf {ROOT_PATH_DOCKER}",
            detach=False,
            interactive=True,
            TTY=False,
        )

        # 把gitHub上的程式碼clone到docker container中
        GITHUB_URL = env_config.GITHUB_URL
        DockerCmd.dockerExec(
            name=CONTAINER_NAME,
            cmd=f"git clone {GITHUB_URL} {ROOT_PATH_DOCKER}",
            detach=False,
            interactive=True,
            TTY=False,
        )

        # CONTAINERNAME - CI
        for root, dirs, files in os.walk(ROOT_PATH_LOCAL):
            rootCheck = False
            for r_ in ["__pycache__", ".git", ".idea", "venv", "OLD"]:
                if root.find(r_) != -1:
                    rootCheck = True
            if rootCheck:
                continue

            DockerCmd.dockerExec(
                name=CONTAINER_NAME,
                cmd=f"mkdir -p {root.replace(ROOT_PATH_LOCAL, ROOT_PATH_DOCKER)}",
                detach=False,
                interactive=True,
                TTY=False,
            )

            for file in files:
                # 把現在執行的程式更新到container中
                DockerCmd.dockerCopy(
                    name=CONTAINER_NAME,
                    filePath=os.path.join(root, file),
                    targetPath=os.path.join(root, file).replace(
                        ROOT_PATH_LOCAL, ROOT_PATH_DOCKER
                    ),
                )

        DockerCmd.dockerExec(
            name=CONTAINER_NAME,
            cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {INTERPRETER} {ROUTE_NAME} local"',
            detach=DEPLOY_DETACH,
            interactive=True,
            TTY=False,
        )
    elif RUN == "local":
        uvicorn.run(app, host="0.0.0.0", port=DEPLOY_PORT)

