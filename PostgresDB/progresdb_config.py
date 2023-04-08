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
PROGRESDB_PYSERVER_PORT = 8002


if __name__ == "__main__":
    # 執行環境
    RUN = "st_admin_course" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "docker_project_build":
        # ---------------------- Deploy: Docker -----------------------
        CONTAINERNAME = "python3.8.16"
        ROOT_PATH_DOCKER = "/Users/peiyuwu/MLOPS"
        ROOT_PATH_LOCAL = "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS"
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

    elif RUN == "docker_deploy":
        # ---------------------- Deploy: Docker -----------------------
        CONTAINERNAME = "python3.8.16"
        INTERPRETER = "python3.8"
        ROOT_PATH_DOCKER = "/Users/peiyuwu/MLOPS"
        ROUTE_PATH = f"{ROOT_PATH_DOCKER}/PostgresDB/route.py"

        # CONTAINERNAME - CD
        DockerCmd.dockerExec(
            name=CONTAINERNAME,
            cmd=f"{INTERPRETER} {ROUTE_PATH} {ROOT_PATH_DOCKER}",
            detach=False,
            interactive=True,
            TTY=False,
        )

    elif RUN == "local_deploy":
        # ---------------------- route: Local 執行，輕鬆就好 -----------------------
        ROOT_PATH_LOCAL = "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS"
        ROUTE_PATH = f"{ROOT_PATH_LOCAL}/PostgresDB/route.py"
        subprocess.run(f"python3 {ROUTE_PATH} {ROOT_PATH_LOCAL}", shell=True)

    elif RUN == "st_create_course_form":
        # ---------------------- route: postgresParseMongodb -----------------------
        PROGRESDB_TABLE = PROGRESDB_TABLE_GOOGLE_FORM
        # PROGRESDB_TABLE = PROGRESDB_TABLE_TEMP
        POST_INFO = {
            "DATA_TIME": DATA_TIME,
            "MONGODB_INFO": {
                "MONGODB_USER": MONGODB_USER,
                "MONGODB_PASSWORD": MONGODB_PASSWORD,
                "MONGODB_HOST": "mongodb",  # route 在 Docker 部署的Host
                # "MONGODB_HOST": MONGODB_HOST, # route 在 Local 部署的Host
                "MONGODB_PORT": MONGODB_PORT,
                "MONGODB_DATABASE": MONGODB_DATABASE,
                "MONGODB_COLLECTION": COLLECTION_GOOGLE_FORM,
                "MONGODB_QUERY": {
                    "dt": {
                        "$gte": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                        "$lt": time.strftime(
                            "%Y-%m-%d", time.localtime(time.time() + 86400)
                        ),
                    }
                },
            },
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
            },
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:{PROGRESDB_PYSERVER_PORT}/PostgresDB/mongodbToProgres/stCreateCourseForm"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:{PROGRESDB_PYSERVER_PORT}/PostgresDB/mongodbToProgres/stCreateCourseForm",
            shell=True,
        )

    elif RUN == "st_admin_course":
        # ---------------------- route: postgresParseMongodb -----------------------
        PROGRESDB_TABLE = PROGRESDB_TABLE_ST_CRAWLER
        # PROGRESDB_TABLE = PROGRESDB_TABLE_TEMP
        POST_INFO = {
            "DATA_TIME": DATA_TIME,
            "MONGODB_INFO": {
                "MONGODB_USER": MONGODB_USER,
                "MONGODB_PASSWORD": MONGODB_PASSWORD,
                "MONGODB_HOST": "mongodb",  # route 在 Docker 部署的Host
                # "MONGODB_HOST": MONGODB_HOST, # route 在 Local 部署的Host
                "MONGODB_PORT": MONGODB_PORT,
                "MONGODB_DATABASE": MONGODB_DATABASE,
                "MONGODB_COLLECTION": COLLECTION_ST_CRAWLER,
                "MONGODB_QUERY": {
                    "dt": {
                        "$gte": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                        "$lt": time.strftime(
                            "%Y-%m-%d", time.localtime(time.time() + 86400)
                        ),
                    }
                },
            },
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
                    "memo": "ST所有課程資料",
                    "commondata1": '"AdminCourses"',
                    "uniquechar1": "開始時間",
                    "uniquechar2": "結束時間",
                    "uniquechar3": "所屬單位",
                    "uniquechar4": "上課地點",
                    "uniquechar5": "年級",
                    "uniquechar6": "課程",
                    "uniquechar7": "老師",
                    "uniquechar8": "學生",
                    "uniquechar9": "課程",
                },
            },
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:{PROGRESDB_PYSERVER_PORT}/PostgresDB/mongodbToProgres/stAdminCourses"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:{PROGRESDB_PYSERVER_PORT}/PostgresDB/mongodbToProgres/stAdminCourses",
            shell=True,
        )
