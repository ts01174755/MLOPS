import os
import sys
import env_config
from STPython_3_8_16.controller.st_google_drive import STGoogleDrive
from STPython_3_8_16.controller.st_line_notify import STLineNotify
from src.model.docker_cmd import DockerCmd
import subprocess
import time
import json
# ---------------------- STEP - params -----------------------
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# 執行環境 - 基本上不需要動
CI_PY_NAME = f'{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/CI_docker_python3_8_16.py'
PY_NAME = f"{env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH}/automation_googleDrive.py"    # 執行的程式
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
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        DATA_TOMORROW = time.strftime("%Y-%m-%d", time.localtime(time.time() + 24 * 60 * 60))
        PROGRESDB_SCHEMA = "original"
        PROGRESDB_TABLE = ["st_all_data", "google_form", "tempdb"][0]
        QUERY_SQL = f"\
            SELECT \
                dt, uniquechar1, uniquechar2, uniquechar3, uniquechar4, \
                uniquechar5, uniquechar6, uniquechar7, uniquechar8 \
            FROM {PROGRESDB_SCHEMA}.{PROGRESDB_TABLE} \
            WHERE 1=1 \
                AND dt >= '{DATA_DAY}' AND dt < '{DATA_TOMORROW}' \
                AND uniquechar3 = '雲課堂' \
                AND uniquechar7 = '羅苡心 Xinn'\
            ORDER BY uniquechar1 DESC;"
        GOOGLE_DRIVE_INFO = {
            "TOKEN": 'env/googleDriveToken_stpeteamshare.json',
            "CLIENT_SECRET_FILE": 'env/client_secret_stpeteamshare.json',
            "SCOPES": ['https://www.googleapis.com/auth/drive'],
        }
        NOTIFY_TOKEN_FILE = 'env/LineNotify.json'
        NOTIFY_TOKEN_TYPE = ['私人Notify', '雲課堂 - Hana'][1]
        PROGRESDB_SCHEMA = PROGRESDB_SCHEMA
        PROGRESDB_TABLE = PROGRESDB_TABLE
        PROGRESDB_SCHEMA_DICT = {
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
        }

        # --------------------- controller ---------------------
        st_google_drive = STGoogleDrive()
        df = st_google_drive.searchPostgres(
            POSTGRESDB=POSTGRESDB,
            QUERY_SQL=QUERY_SQL,
        )

        # 撰寫 googleDrive 模擬cd, rm, mkdir, 等shell操作
        notifyInfo = st_google_drive.fileMoveAndCopy(
            GOOGLE_DRIVE_INFO=GOOGLE_DRIVE_INFO,
            df=df
        )
        if len(notifyInfo) == 0:
            print("無資料更新")
            sys.exit(0)

        line_message = st_google_drive.line_notify_message(notifyInfo)

        with open(NOTIFY_TOKEN_FILE, 'r') as f:
            lineNotifyToken = json.load(f)

        st_line_notify = STLineNotify()
        st_line_notify.postLineNotify(
            token=lineNotifyToken[NOTIFY_TOKEN_TYPE],
            message=line_message
        )
