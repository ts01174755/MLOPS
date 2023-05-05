import os
import sys
import env_config
from MongoDB.controller.mongodb_crawler_data import CrawlerData
from MongoDB.controller.mongodb_googleform_data import GoogleFormData
from src.model.docker_cmd import DockerCmd
import subprocess
import time

# ---------------------- STEP - params -----------------------
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# 執行環境 - 基本上不需要動
CI_PY_NAME = f'{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/CI_docker_python3_8_16.py'
PY_NAME = f"{env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH}/automation_datalake_crawler.py"    # 執行的程式
if RUN == "docker":
    # ------------------------ env_params ------------------------
    LOCAL_INTERPRETER = env_config.MLOPS_ROOT_PATH_LOCAL_INTERPRETER
    subprocess.run(f"{LOCAL_INTERPRETER} {CI_PY_NAME}", shell=True)

    CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_NAME     # 執行環境
    ROOT_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH    # DOCKER 執行路徑
    DOCKER_INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_INTERPRETER      # 執行的python解釋器
    DockerCmd.dockerExec(
        name=CONTAINER_NAME,
        cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {DOCKER_INTERPRETER} {PY_NAME} local"',
        detach=False,
        interactive=True,
        TTY=False,
    )


if __name__ == "__main__":
    # --------------------- controller env params ---------------------
    MONGODB = env_config.MONGODB_DOCKER  # mongodb連線資訊
    # MONGODB = env_config.MONGODB_LOCAL    # mongodb連線資訊
    POSTGRESDB = env_config.POSTGRESDB_DOCKER  # postgres連線資訊
    # POSTGRESDB = env_config.POSTGRESDB_LOCAL  # postgres連線資訊
    PROJECT_PATH = env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH  # 存放資料的位置
    # PROJECT_PATH = env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH  # 存放資料的位置
    FILE_PATH = env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH  # 存放資料的位置
    # FILE_PATH = env_config.MLOPS_ROOT_PATH_LOCAL_FILE_PATH  # 存放資料的位置
    DOWNLOAD_PATH = env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH  # 存放資料的位置
    # DOWNLOAD_PATH = env_config.MLOPS_ROOT_PATH_LOCAL_DOWNLOAD_PATH  # 存放資料的位置

    if RUN == "local":
        # --------------------- controller params ---------------------
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        URL = os.getenv("ST_ALLURL")
        COOKIES = {"ST": os.getenv("ST_TOKEN")}
        COLLECTION = ["st_all_data", "tempdb", "google_form"][0]

        # --------------------- controller ---------------------
        crawler_data = CrawlerData()
        crawler_data.get_crawlerdata_to_mongodb(
            URL=URL,
            COOKIES=COOKIES,
            Mongodb=MONGODB,
            COLLECTION=COLLECTION,
            DATATIME=DATA_TIME,
        )

        # --------------------- controller params ---------------------
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        TOKEN = "env/token.json"
        CLIENT_SECRET_FILE = "env/client_secret.json"
        SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
        DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
        COLLECTION = ["st_all_data", "tempdb", "google_form"][2]
        FORMID = "1sqxcABwDaVFyGD1cTo0-O0BoJIGWJccioaXGkxKMZv8"

        # --------------------- controller ---------------------
        google_form_data = GoogleFormData()
        google_form_data.get_googleformdata_to_mongodb(
            TOKEN=TOKEN,
            CLIENT_SECRET_FILE=CLIENT_SECRET_FILE,
            SCOPES=SCOPES,
            DISCOVERY_DOC=DISCOVERY_DOC,
            Mongodb=MONGODB,
            COLLECTION=COLLECTION,
            FORMID=FORMID,
            DATATIME=DATA_TIME,
        )

        for i in range(1, 0, -1):
            # --------------------- controller params ---------------------
            DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            DATA_DAY = time.strftime("%Y_%m_%d", time.localtime(time.time() - 86400 * i))
            FILE_NAME = f"Daily_{DATA_DAY}.zip"
            URL = f"https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/{FILE_NAME}"  # 下載檔案的網址
            FILENAME = f"{FILE_NAME.split('.')[0]}"  # 下載檔案的路徑

            # --------------------- controller ---------------------
            crawler_data = CrawlerData()
            crawler_data.get_crawlerZipFile_to_fileSystem(
                URL=URL,
                FILEPATH=f'{DOWNLOAD_PATH}/{FILENAME}',
            )