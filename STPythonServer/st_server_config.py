import os
import sys

sys.path.append(
    "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/venv/lib/python3.9/site-packages"
)
sys.path.append("/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS")
import time
from dotenv import load_dotenv, find_dotenv
from src.my_model.docker_cmd import DockerCmd
import subprocess
import json
import pandas as pd

# 顯示pandas所有欄位
pd.set_option("display.max_columns", None)

load_dotenv(find_dotenv("env/.env"))

# ---------------------- Global -----------------------
DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
DATA_TOMORROW = time.strftime(
    "%Y-%m-%d", time.localtime(time.time() + 24 * 60 * 60)
)
MONGODB_PORT = int(os.getenv("MongoDB_PORT"))
MONGODB_HOST = os.getenv("MongoDB_HOST")
MONGODB_USER = os.getenv("MongoDB_USER")
MONGODB_PASSWORD = os.getenv("MongoDB_PASSWORD")
MONGODB_DATABASE = "originaldb"
PROGRESDB_PORT = int(os.getenv("POSTGRES_PORT"))
PROGRESDB_HOST = os.getenv("POSTGRES_HOST")
PROGRESDB_USER = os.getenv("POSTGRES_USER")
PROGRESDB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PROGRESDB_DATABASE = "originaldb"
PROGRESDB_SCHEMA = "original"
PROGRESDB_TABLE_ST_CRAWLER = "st_all_data"
PROGRESDB_TABLE_TEMP = "temptb"
PROGRESDB_TABLE_GOOGLE_FORM = "google_form"
COLLECTION_ST_CRAWLER = "st_all_data"
COLLECTION_TEMPDB = "tempdb"
COLLECTION_GOOGLE_FORM = "google_form"
ST_PYSERVER_PORT = 8003

CONTAINERNAME = "python3.8.16"
ROOT_PATH_DOCKER = "/Users/peiyuwu/MLOPS"
ROOT_PATH_LOCAL = "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS"
ROUTE_DOCKER_PATH = f"{ROOT_PATH_DOCKER}/STPythonServer/route.py"
ROUTE_LOCKER_PATH = f"{ROOT_PATH_LOCAL}/STPythonServer/route.py"


if __name__ == "__main__":
    # 執行環境
    RUN = "None" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "docker_project_build":
        # ---------------------- Deploy: Docker -----------------------
        GITHUB_URL = "https://github.com/ts01174755/MLOPS.git"
        # 重啟docker container
        DockerCmd.dockerRestart(CONTAINERNAME)

        # 移除container中的舊程式
        DockerCmd.dockerExec(
            name=CONTAINERNAME,
            cmd=f"rm -rf {ROOT_PATH_DOCKER}",
            detach=False,
            interactive=True,
            TTY=False,
        )

        # 把gitHub上的程式碼clone到docker container中
        DockerCmd.dockerExec(
            name=CONTAINERNAME,
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
                name=CONTAINERNAME,
                cmd=f"mkdir -p {root.replace(ROOT_PATH_LOCAL, ROOT_PATH_DOCKER)}",
                detach=False,
                interactive=True,
                TTY=False,
            )

            for file in files:
                # 把現在執行的程式更新到container中
                DockerCmd.dockerCopy(
                    name=CONTAINERNAME,
                    filePath=os.path.join(root, file),
                    targetPath=os.path.join(root, file).replace(
                        ROOT_PATH_LOCAL, ROOT_PATH_DOCKER
                    ),
                )

    RUN = "docker_deploy" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "docker_deploy":
        # ---------------------- Deploy: Docker -----------------------
        CONTAINERNAME = "python3.8.16"
        INTERPRETER = "python3.8"

        # CONTAINERNAME - CD
        DockerCmd.dockerExec(
            name=CONTAINERNAME,
            cmd=f"{INTERPRETER} {ROUTE_DOCKER_PATH} {ROOT_PATH_DOCKER}",
            detach=True,
            interactive=True,
            TTY=False,
        )
    elif RUN == "local_deploy":
        # ---------------------- route: Local 執行，輕鬆就好 -----------------------
        # 重啟docker container
        DockerCmd.dockerStop(CONTAINERNAME)
        subprocess.run(f"python3 {ROUTE_LOCKER_PATH} {ROOT_PATH_LOCAL}", shell=True)

    RUN = "None" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "st_google_drive":
        # ---------------------- route: postgresParseMongodb -----------------------
        PROGRESDB_TABLE = PROGRESDB_TABLE_ST_CRAWLER
        # PROGRESDB_TABLE = PROGRESDB_TABLE_TEMP
        QUERY_SQL = f'\
        SELECT \
            dt, uniquechar1, uniquechar2, uniquechar3, uniquechar4, \
            uniquechar5, uniquechar6, uniquechar7, uniquechar8 \
            FROM {PROGRESDB_SCHEMA}.{PROGRESDB_TABLE} \
            WHERE 1=1 \
                AND dt >= "{DATA_DAY}" AND dt < "{DATA_TOMORROW}" \
                AND uniquechar3 = "雲課堂" \
                AND uniquechar7 = "羅苡心 Xinn"\
            ORDER BY uniquechar1 DESC;'
        POST_INFO = {
            "DEFAULT_DICT": {
                "DATA_DAY": DATA_DAY,
                "GOOGLE_DRIVE_INFO": {
                    "TOKEN": 'env/googleDriveToken_stpeteamshare.json',
                    "CLIENT_SECRET_FILE": 'env/client_secret_stpeteamshare.json',
                    "SCOPES": ['https://www.googleapis.com/auth/drive'],
                },
                "NOTIFY_TOKEN_FILE": 'env/LineNotify.json',
                "NOTIFY_TOKEN_TYPE": '雲課堂 - Hana',
                # "NOTIFY_TOKEN_TYPE": '私人Notify',
                "PROGRESDB_INFO": {
                    "POSTGRES_USER": PROGRESDB_USER,
                    "POSTGRES_PASSWORD": PROGRESDB_PASSWORD,
                    "POSTGRES_HOST": "postgres15.2",  # route 在 Docker 部署的Host
                    # 'POSTGRES_HOST': PROGRESDB_HOST, # route 在 Local 部署的Host
                    "POSTGRES_PORT": PROGRESDB_PORT,
                    "POSTGRES_DATABASE": PROGRESDB_DATABASE,
                    "PROGRESDB_SCHEMA": PROGRESDB_SCHEMA,
                    "PROGRESDB_TABLE": PROGRESDB_TABLE,
                    "PROGRESDB_SCHEMA_FILE_PATH": f"/Users/peiyuwu/Files/GoogleFormDataSchema_{PROGRESDB_TABLE}.csv",
                    "PROGRESDB_SCHEMA_DICT": {
                        "dt": "資料更新時間",
                        "memo": "新申請課程",
                        "commondata1": '"GoogleForm表單"',
                        "uniquechar1": "填表日",
                        "uniquechar2": "申請人(Email)",
                        "uniquechar3": "所屬單位",
                        "uniquechar4": "上課地點",
                        "uniquechar5": "年級",
                        "uniquechar6": "課程",
                        "uniquechar7": "老師",
                        "uniquechar8": "學生",
                    },
                    "QUERY_SQL": QUERY_SQL
                }
            }
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:{ST_PYSERVER_PORT}/stPythonServer/stGoogleDrive"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:{ST_PYSERVER_PORT}/stPythonServer/stGoogleDrive",
            shell=True,
        )
