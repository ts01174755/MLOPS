import os
import sys
import env_config
from PostgresDB.controller.postgres_parse_mongodb_data import PosgresParseMongodbData
from src.model.docker_cmd import DockerCmd
import subprocess
import time

# ---------------------- STEP - params -----------------------
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# 執行環境 - 基本上不需要動
CI_PY_NAME = f'{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/CI_docker_python3_8_16.py'
PY_NAME = f"{env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH}/automation_datawarehouse_crawler.py"    # 執行的程式
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
        MONGODB_COLLECTION = ["google_form", "tempdb"][0]
        MONGODB_QUERY = {
            "dt": {
                "$gte": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                "$lt": time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400))
            }
        }
        PROGRESDB_TABLE = ["google_form", "tempdb"][0]
        PROGRESDB_SCHEMA = "original"
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
        # 每日執行 - 爬蟲
        posgresParseMongodbData = PosgresParseMongodbData()
        googleFormDF = posgresParseMongodbData.parseGoogleSTFromData(
            MONGODB=MONGODB,
            DATA_TIME=DATA_TIME,
            MONGODB_COLLECTION=MONGODB_COLLECTION,
            MONGODB_QUERY=MONGODB_QUERY,
            PROGRESDB_SCHEMA_DICT=PROGRESDB_SCHEMA_DICT,
        )

        # 連接PostgresDB與寫入資料
        posgresParseMongodbData.insertPostgresData(
            PROGRESDB=POSTGRESDB,
            PROGRESDB_TABLE=PROGRESDB_TABLE,
            PROGRESDB_SCHEMA=PROGRESDB_SCHEMA,
            dataFrame=googleFormDF,
        )

        # --------------------- controller params ---------------------
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        MONGODB_COLLECTION = ["st_all_data", "tempdb"][0]
        PROGRESDB_SCHEMA = "original"
        PROGRESDB_TABLE = ["st_all_data", "tempdb"][0]
        MONGODB_QUERY = {
            "dt": {
                "$gte": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                "$lt": time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400))
            }
        }
        PROGRESDB_SCHEMA_DICT = {
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
        }

        # --------------------- controller ---------------------
        # 每日執行 - 爬蟲
        posgresParseMongodbData = PosgresParseMongodbData()
        googleFormDF = posgresParseMongodbData.parseSTData(
            MONGODB=MONGODB,
            MONGODB_COLLECTION=MONGODB_COLLECTION,
            MONGODB_QUERY=MONGODB_QUERY,
            PROGRESDB_SCHEMA_DICT=PROGRESDB_SCHEMA_DICT,
            DATA_TIME=DATA_TIME,
        )

        # 連接PostgresDB與寫入資料
        posgresParseMongodbData.insertPostgresData(
            PROGRESDB=POSTGRESDB,
            dataFrame=googleFormDF,
            PROGRESDB_TABLE=PROGRESDB_TABLE,
            PROGRESDB_SCHEMA=PROGRESDB_SCHEMA,
        )

        # --------------------- controller params ---------------------
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        MONGODB_COLLECTION = ["st_all_data", "tempdb"][0]
        PROGRESDB_SCHEMA = "original"
        PROGRESDB_TABLE = ["st_all_data", "tempdb"][0]
        COLUMNS_LIST = [
            "dt", "memo",
            "commondata1", "commondata2", "commondata3", "commondata4", "commondata5",
            "commondata6", "commondata7", "commondata8", "commondata9", "commondata10",
            "uniquechar1", "uniquechar2", "uniquechar3", "uniquechar4", "uniquechar5",
            "uniquechar6", "uniquechar7", "uniquechar8", "uniquechar9", "uniquechar10",
            "uniqueint1", "uniqueint2", "uniqueint3", "uniqueint4", "uniqueint5",
            "uniqueint6", "uniqueint7", "uniqueint8", "uniqueint9", "uniqueint10",
            "uniquefloat1", "uniquefloat2", "uniquefloat3", "uniquefloat4", "uniquefloat5",
            "uniquefloat6", "uniquefloat7", "uniquefloat8", "uniquefloat9", "uniquefloat10",
            "uniquefloat11", "uniquefloat12", "uniquefloat13", "uniquefloat14", "uniquefloat15",
            "uniquestring1", "uniquestring2", "uniquestring3", "uniquestring4", "uniquestring5", "uniquejason",
        ]
        PROGRESDB_SCHEMA_FILE = f"{PROGRESDB_SCHEMA}.{PROGRESDB_TABLE}.csv"
        PROGRESDB_SCHEMA_DICT = {
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
        }

        # --------------------- controller ---------------------
        posgresParseMongodbData = PosgresParseMongodbData()
        posgresParseMongodbData.makeDataSchema(
            PROGRESDB=POSTGRESDB,
            tableName=PROGRESDB_TABLE,
            schemaDict=PROGRESDB_SCHEMA_DICT,
            columnList=COLUMNS_LIST,
            schemaFilePath=f'{FILE_PATH}/{PROGRESDB_SCHEMA_FILE}',
        )