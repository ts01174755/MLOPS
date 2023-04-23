import os
import sys
import env_config
from MongoDB.controller.mongodb_crawler_data import CrawlerData
from MongoDB.controller.mongodb_googleform_data import GoogleFormData
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging
from src.model.docker_cmd import DockerCmd
# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8001
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# ------------------------ env_params ------------------------
CONTAINER_NAME = env_config.CONTAINERNAME_PYTHON_3_8_18     # 執行環境
ROOT_PATH_DOCKER = env_config.CONTAINERNAME_ROOT_PATH_DOCKER    # DOCKER 執行路徑
ROOT_PATH_LOCAL = env_config.CONTAINERNAME_ROOT_PATH_LOCAL      # LOCAL 執行路徑
INTERPRETER = env_config.CONTAINER_INTERPRETER      # 執行的python解釋器
ROUTE_NAME = f"{ROOT_PATH_DOCKER}/build_crawler_server.py"    # 執行的程式
LOG_PATH = f"{ROOT_PATH_DOCKER}/log_crawler_server.log"    # 執行的程式
MONGODB = env_config.MONGODB_DOCKER     # mongodb連線資訊
# MONGODB = env_config.MONGODB_LOCAL    # mongodb連線資訊
DEPLOY_DETACH = True

# ------------------------- ROUTE ----------------------------
app = FastAPI()

if RUN == "local":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler()
        ]
    )

class STCrawlerRequestBody(BaseModel):
    DATA_TIME: str = None
    URL: str = None
    COOKIES: dict = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None
    MONGODB_PORT: int = None
    MONGODB_HOST: str = None
    MONGODB_DATABASE: str = None
    COLLECTION: str = None


class CrawlerFileRequestBody(BaseModel):
    URL: str = None
    FILEPATH: str = None


class GoogleFormDataRequestBody(BaseModel):
    DATA_TIME: str = None
    TOKEN: str = None
    CLIENT_SECRET_FILE: str = None
    SCOPES: str = None
    FORMID: str = None
    DISCOVERY_DOC: str = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None
    MONGODB_PORT: int = None
    MONGODB_HOST: str = None
    MONGODB_DATABASE: str = None
    COLLECTION: str = None


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.post("/MongoDB/crawlerDataPost")
def crawler_data_post(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    crawler_data = CrawlerData()

    # 爬蟲
    crawler_data.get_crawlerdata_to_mongodb(
        URL=params.URL,
        COOKIES=params.COOKIES,
        Mongodb = MONGODB,
        COLLECTION=params.COLLECTION,
        DATATIME=params.DATA_TIME,
    )
    return {"message": "insert success"}


@app.post("/MongoDB/crawlerZipFilePost")
def crawler_zip_file_post(params: CrawlerFileRequestBody = CrawlerFileRequestBody()):
    crawler_data = CrawlerData()

    # 爬蟲
    crawler_data.get_crawlerZipFile_to_fileSystem(
        URL=params.URL,
        FILEPATH=params.FILEPATH,
    )
    return {"message": "insert success"}


@app.post("/MongoDB/googleFormDataPost")
def google_form_data_post(params: GoogleFormDataRequestBody = GoogleFormDataRequestBody()):
    google_form_data = GoogleFormData()

    google_form_data.get_googleformdata_to_mongodb(
        TOKEN=params.TOKEN,
        CLIENT_SECRET_FILE=params.CLIENT_SECRET_FILE,
        SCOPES=params.SCOPES,
        DISCOVERY_DOC=params.DISCOVERY_DOC,
        Mongodb = MONGODB,
        COLLECTION=params.COLLECTION,
        FORMID=params.FORMID,
        DATATIME=params.DATA_TIME,
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
