import os
import sys
import pandas as pd
import env_config
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import aiofiles
import uvicorn
import logging
import json
from STPython_3_8_16_Server.contorller.pythonChatServer import PythonChatServer, CustomJSONResponse
from src.controller.logger import LoggingMiddleware
from src.model.docker_cmd import DockerCmd
import subprocess
from pprint import pprint
import time

# ---------------------- STEP - params -----------------------
DEPLOY_PORT = 8000
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

# 執行環境 - 基本上不需要動
CI_PY_NAME = f'{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/CI_docker_python3_8_16_server.py'
PY_NAME = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st.py"    # 執行的程式
DEPLOY_DETACH = False
if RUN == "docker":
    # ------------------------ env_params ------------------------
    LOCAL_INTERPRETER = env_config.MLOPS_ROOT_PATH_LOCAL_INTERPRETER
    subprocess.run(f"{LOCAL_INTERPRETER} {CI_PY_NAME}", shell=True)

    CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_SERVER_NAME     # 執行環境
    ROOT_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH    # DOCKER 執行路徑
    DOCKER_INTERPRETER = env_config.CONTAINER_PYTHON_3_8_18_SERVER_INTERPRETER      # 執行的python解釋器
    DockerCmd.dockerExec(
        name=CONTAINER_NAME,
        cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {DOCKER_INTERPRETER} {PY_NAME} docker_local"',
        detach=DEPLOY_DETACH,
        interactive=True,
        TTY=False,
    )

# --------------------- controller env params ---------------------
MONGODB = env_config.MONGODB_DOCKER if RUN.find('docker') != -1 else env_config.MONGODB_LOCAL    # mongodb連線資訊
POSTGRESDB = env_config.POSTGRESDB_DOCKER if RUN.find('docker') != -1 else env_config.POSTGRESDB_LOCAL   # postgres連線資訊
PROJECT_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH  # 存放資料的位置
FILE_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_FILE_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_FILE_PATH  # 存放資料的位置
DOWNLOAD_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_DOWNLOAD_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_DOWNLOAD_PATH  # 存放資料的位置
LOG_PATH = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st_log.log" if RUN.find('docker') != -1 else f"{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/server_st_log.log"   # 執行的程式

# ------------------------- ROUTE ----------------------------
if RUN.find('local') != -1:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler()
        ]
    )

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
        '指考化學影片課程規劃': '0014',
        '指考物理影片課程規劃': '0015',
        '學測生物影片課程規劃': '0016',
        '學測英文影片課程規劃': '0017',
        '學測國文影片課程規劃（古文十五+文化經典教材）': '0018',
        '學測國文影片課程規劃（學測總複習）': '0019',
        '學測數A影片課程規劃': '0020',
    }
    course_detail_dict = {}
    course_count = 0
    data = []
    for course_, course_code_ in course_code_dict.items():
        with open(f"{PROJECT_PATH}/STPython_3_8_16_Server/files/{course_}.json", "r", encoding="utf-8") as f:
            course_detail_dict[course_code_] = json.load(f)
            # 計算課程數目
            for course_ind_, courses_ in course_detail_dict[course_code_].items():
                course_count += len(courses_)
                for url_name_, url_list_ in courses_.items():
                    for url_ in url_list_:
                        data.append([course_, course_ind_, url_name_, url_])

    course_df = pd.DataFrame(data, columns=["course", "course_ind", "url_name", "url"])
    file_name = '課程列表.xlsx'
    course_df.to_excel(f"{PROJECT_PATH}/STPython_3_8_16_Server/files/{file_name}", index=False, engine='openpyxl')
    print(f"現在有的影片數: {course_count}")

app = FastAPI()
app.add_middleware(LoggingMiddleware)
manager = PythonChatServer()


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.get("/stCloudCourse/totalCourse")
def get_total_course():
    return CustomJSONResponse(content=data)


@app.get("/stCloudCourse/courseCollection", response_class=HTMLResponse)
async def get():
    async with aiofiles.open(f"{PROJECT_PATH}/STPython_3_8_16_Server/template/index.html", mode="r") as f:
        content = await f.read()
    return HTMLResponse(content=content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.insert_document_mongdb(
                mongoDBCtrl=MONGODB,
                collection='course_collection',
                document={
                    "from": 'python_st_server',
                    "dt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "data": data
                }
            )
            await manager.send_message(f"Client: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

if __name__ == "__main__":
    if RUN.find('local') != -1:
        uvicorn.run(app, host="0.0.0.0", port=DEPLOY_PORT)
