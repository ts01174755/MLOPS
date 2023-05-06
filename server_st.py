import os
import sys
import env_config
from fastapi import FastAPI
from starlette.responses import JSONResponse
import uvicorn
import logging
import json
from src.controller.logger import LoggingMiddleware
from src.model.docker_cmd import DockerCmd
import subprocess
from pprint import pprint

# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8000
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# 執行環境 - 基本上不需要動
CI_PY_NAME = f'{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/CI_docker_python3_8_16_server.py'
PY_NAME = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st.py"    # 執行的程式
DEPLOY_DETACH = True
if RUN == "docker":
    # ------------------------ env_params ------------------------
    LOCAL_INTERPRETER = env_config.MLOPS_ROOT_PATH_LOCAL_INTERPRETER
    subprocess.run(f"{LOCAL_INTERPRETER} {CI_PY_NAME}", shell=True)

    CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_SERVER_NAME     # 執行環境
    ROOT_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH    # DOCKER 執行路徑
    DOCKER_INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_SERVER_INTERPRETER      # 執行的python解釋器
    DockerCmd.dockerExec(
        name=CONTAINER_NAME,
        cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {DOCKER_INTERPRETER} {PY_NAME} local"',
        detach=DEPLOY_DETACH,
        interactive=True,
        TTY=False,
    )

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
LOG_PATH = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st_log.log"    # 執行的程式
# LOG_PATH = f"{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/server_st_log.log"    # 執行的程式


class CustomJSONResponse(JSONResponse):

    def __init__(self, content: any, *args, **kwargs):
        super().__init__(content, *args, **kwargs)
        self.headers["Content-Type"] = "application/json; charset=utf-8"

    def render(self, content: any) -> bytes:
        return json.dumps(content, ensure_ascii=False, allow_nan=False, indent=None, separators=(",", ":")).encode("utf-8")



# ------------------------- ROUTE ----------------------------
if RUN == "local":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler()
        ]
    )

app = FastAPI()
app.add_middleware(LoggingMiddleware)


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.get("/stCloudCourse/totalCourse")
def get_total_course():
    course_code_dict = {
        '國一數學(一)影片課程規劃': '0001',
        '國一數學(二)影片課程規劃': '0002',
        '國二數學(三)影片課程規劃': '0003',
        '國二數學(四)影片課程規劃': '0004',
        '國二理化(三)影片課程規劃': '0005',
        '國二理化(四)影片課程規劃': '0006',
        '多益課程影片規劃': '0007',
        '多益閱讀題型': '0008',
        '學測化學影片課程規劃': '0009',
        '學測國文影片課程規劃': '0010',
        '學測地科影片課程規劃': '0011',
        '學測數學影片課程規劃': '0012',
        '學測物理影片課程規劃': '0013',
    }
    return CustomJSONResponse(content=course_code_dict)


@app.get("/stCloudCourse/{courseCode}")
def get_course_by_code(courseCode: str):
    course_code_reverse_dict = {
        '0001': '國一數學(一)影片課程規劃',
        '0002': '國一數學(二)影片課程規劃',
        '0003': '國二數學(三)影片課程規劃',
        '0004': '國二數學(四)影片課程規劃',
        '0005': '國二理化(三)影片課程規劃',
        '0006': '國二理化(四)影片課程規劃',
        '0007': '多益課程影片規劃',
        '0008': '多益閱讀題型',
        '0009': '學測化學影片課程規劃',
        '0010': '學測國文影片課程規劃',
        '0011': '學測地科影片課程規劃',
        '0012': '學測數學影片課程規劃',
        '0013': '學測物理影片課程規劃'
    }
    # 依據course_detail_dict[key]取得value
    # value是 /Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/STPython_3_8_16_Server/files/xxx.json 的檔案名稱xxx
    # 讀成dict後回傳
    course_detail_dict = {}
    for course_code_, course_ in course_code_reverse_dict.items():
        with open(f"{PROJECT_PATH}/STPython_3_8_16_Server/files/{course_}.json", "r", encoding="utf-8") as f:
            course_detail_dict[course_code_] = json.load(f)
    pprint(course_detail_dict)

    return CustomJSONResponse(content=course_detail_dict[courseCode])


if __name__ == "__main__":

    if RUN == "local":
        uvicorn.run(app, host="0.0.0.0", port=DEPLOY_PORT)