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

load_dotenv(find_dotenv("env/.env"))

# ---------------------- Global -----------------------
DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())

MONGODB_PORT = int(os.getenv("MongoDB_PORT"))
MONGODB_HOST = os.getenv("MongoDB_HOST")
MONGODB_USER = os.getenv("MongoDB_USER")
MONGODB_PASSWORD = os.getenv("MongoDB_PASSWORD")
MONGODB_DATABASE = "originaldb"
COLLECTION_ST_CRAWLER = "st_all_data"
COLLECTION_TEMPDB = "tempdb"
COLLECTION_GOOGLE_FORM = "google_form"
MONGODB_PYSERVER_PORT = 8001

CONTAINERNAME = "python3.8.16"
ROOT_PATH_DOCKER = "/Users/peiyuwu/MLOPS"
ROOT_PATH_LOCAL = "/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS"
ROUTE_DOCKER_PATH = f"{ROOT_PATH_DOCKER}/MongoDB/route.py"
ROUTE_LOCKER_PATH = f"{ROOT_PATH_LOCAL}/MongoDB/route.py"


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

    RUN = "None" if len(sys.argv) == 1 else sys.argv[1]
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

    RUN = "google_form" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "st_crawler":
        # ---------------------- route: st_crawler -----------------------
        ST_CRAWLER_DATA = {
            "DATA_TIME": DATA_TIME,
            "URL": os.getenv("ST_ALLURL"),
            "COOKIES": {"ST": os.getenv("ST_TOKEN")},
            "MONGODB_USER": MONGODB_USER,
            "MONGODB_PASSWORD": MONGODB_PASSWORD,
            "MONGODB_PORT": MONGODB_PORT,
            "MONGODB_HOST": "mongodb",  # route 在 Docker 部署的Host
            # "MONGODB_HOST": MONGODB_HOST, # route 在 Local 部署的Host
            "MONGODB_DATABASE": MONGODB_DATABASE,
            "COLLECTION": COLLECTION_ST_CRAWLER,
            # "COLLECTION": COLLECTION_TEMPDB,
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(ST_CRAWLER_DATA)}' http://localhost:{MONGODB_PYSERVER_PORT}/MongoDB/crawlerDataPost"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(ST_CRAWLER_DATA)}' http://localhost:{MONGODB_PYSERVER_PORT}/MongoDB/crawlerDataPost",
            shell=True,
        )

    elif RUN == "google_form":
        # ---------------------- route: GoogleFormData -----------------------
        GOOGLEFORM_DATA = {
            "DATA_TIME": DATA_TIME,
            "TOKEN": f"env/token.json",
            "CLIENT_SECRET_FILE": f"env/client_secret.json",
            "SCOPES": "https://www.googleapis.com/auth/forms.responses.readonly",
            "FORMID": "1sqxcABwDaVFyGD1cTo0-O0BoJIGWJccioaXGkxKMZv8",
            "DISCOVERY_DOC": "https://forms.googleapis.com/$discovery/rest?version=v1",
            "MONGODB_USER": MONGODB_USER,
            "MONGODB_PASSWORD": MONGODB_PASSWORD,
            "MONGODB_PORT": MONGODB_PORT,
            "MONGODB_HOST": "mongodb",  # route 在 Docker 部署的Host
            # "MONGODB_HOST": MONGODB_HOST,  # route 在 Local 部署的Host
            "MONGODB_DATABASE": MONGODB_DATABASE,
            "COLLECTION": COLLECTION_GOOGLE_FORM,
            # "COLLECTION": COLLECTION_TEMPDB,
        }

        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(GOOGLEFORM_DATA)}' http://localhost:{MONGODB_PYSERVER_PORT}/MongoDB/googleFormDataPost"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(GOOGLEFORM_DATA)}' http://localhost:{MONGODB_PYSERVER_PORT}/MongoDB/googleFormDataPost",
            shell=True,
        )

    elif RUN == "futuresExchange":
        # ---------------------- route: FuturesExchangeData -----------------------
        DATA_DAY = time.strftime("%Y_%m_%d", time.localtime())
        FILE_NAME = f"Daily_{DATA_DAY}.zip"
        FUTURES_EXCHANGE_DATA = {
            "URL": f"https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/{FILE_NAME}",  # 下載檔案的網址
            "FILEPATH": f"/Users/peiyuwu/Downloads/{FILE_NAME.split('.')[0]}",  # 下載檔案的路徑
        }

        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(FUTURES_EXCHANGE_DATA)}' http://localhost:{MONGODB_PYSERVER_PORT}/MongoDB/crawlerZipFilePost"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(FUTURES_EXCHANGE_DATA)}' http://localhost:{MONGODB_PYSERVER_PORT}/MongoDB/crawlerZipFilePost",
            shell=True,
        )
