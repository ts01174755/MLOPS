import os
import sys
import pandas as pd
import env_config
from starlette.concurrency import run_in_threadpool
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import aiofiles
import uvicorn
import logging
import json
from STPython_3_8_16_Server.contorller.py_server import PythonChatServer, CustomJSONResponse
from STPython_3_8_16_Server.contorller.yt_video_info import YtVideoInfo
from src.controller.logger import LoggingMiddleware
from src.model.docker_cmd import DockerCmd
from src.model.cicd import CICD
import subprocess
import time

# --------------------- controller params ---------------------
DEPLOY_PORT = 8000
RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
# RUN = "local"

MONGODB = env_config.MONGODB_DOCKER if RUN.find('docker') != -1 else env_config.MONGODB_LOCAL  # mongodb連線資訊
POSTGRESDB = env_config.POSTGRESDB_DOCKER if RUN.find('docker') != -1 else env_config.POSTGRESDB_LOCAL  # postgres連線資訊
PROJECT_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH  # 存放資料的位置
FILE_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_FILE_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_FILE_PATH  # 存放資料的位置
DOWNLOAD_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_DOWNLOAD_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_DOWNLOAD_PATH  # 存放資料的位置
LOG_PATH = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st_log.log" if RUN.find('docker') != -1 else f"{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/server_st_log.log"  # 執行的程式

# --------------------- docker env_params ---------------------
# 執行環境 - 基本上不需要動
if RUN == "docker":
    cicd = CICD(
        local_path=env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH,
        docker_path=env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH,
        container_name=env_config.CONTAINER_PYTHON_3_8_18_SERVER_NAME,
        container_interpreter=env_config.CONTAINER_PYTHON_3_8_18_SERVER_INTERPRETER,
        gitHub_url=env_config.GITHUB_URL,
        folder_ignore_list=["__pycache__", ".git", ".idea", "venv", "OLD"]
    )
    cicd.ci_run()
    cicd.cd_run(
        py_name=f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st.py",
        py_params="docker_local",
        detach=True
    )


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

app = FastAPI()
app.add_middleware(LoggingMiddleware)
manager = PythonChatServer()
yt_collection_manager = PythonChatServer()

# Mount static files
app.mount("/css", StaticFiles(directory="STPython_3_8_16_Server/css"), name="css")
app.mount("/js", StaticFiles(directory="STPython_3_8_16_Server/js"), name="js")
app.mount("/template", StaticFiles(directory="STPython_3_8_16_Server/template"), name="template")


# 部署測試服務
@app.get("/")
async def get_index():
    async with aiofiles.open("STPython_3_8_16_Server/template/index.html", mode="r") as file_reader:
        content = await file_reader.read()
    return HTMLResponse(content=content)


@app.get("/stCloudCourse/totalCourse")
def get_total_course():
    MONDODB_QUERY = {"from": "init_course_collection"}
    data = MONGODB.find_document(
        collection_name='course_collection',
        query=MONDODB_QUERY
    )
    return CustomJSONResponse(content=data[0]['data'])


# @app.get("/stCloudCourse/courseCollection", response_class=HTMLResponse)
# async def course_collection():
#     async with aiofiles.open(f"{PROJECT_PATH}/STPython_3_8_16_Server/template/course_collection.html", mode="r") as f:
#         content = await f.read()
#     return HTMLResponse(content=content)


@app.websocket("/stCloudCourse/courseCollection/ws")
async def course_collection_wsed(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(data)
            await manager.insert_document_mongdb(
                mongoDBCtrl=MONGODB,
                collection='course_collection',
                document={
                    "from": 'python_st_server',
                    "dt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "data": data
                }
            )
            await manager.send_message(json.dumps({'Client': {data}}))
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


# @app.get("/stCloudCourse/ytChannelPlaylistCollection", response_class=HTMLResponse)
# async def get_yt_channel_playlist_collection(request: Request):
#     async with aiofiles.open(
#             f"{PROJECT_PATH}/STPython_3_8_16_Server/template/chanellPlaylistCollection.html", mode="r"
#     ) as file_reader:
#         content = await file_reader.read()
#     return HTMLResponse(content=content)


@app.websocket("/stCloudCourse/ytChannelPlaylistCollection/ws")
async def yt_channel_playlist_collection_wsed(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()
            message_data = json.loads(message)

            if message_data["action"] == "submit_course":
                course_data = message_data["data"]
                providerName = course_data["providerName"]
                courseCategory = course_data["courseCategory"]
                courseName = course_data["courseName"]
                channel_url = course_data["courseUrl"]
                courseContent = course_data["courseContent"]
                all_playlist = await YtVideoInfo.get_channel_playlists_info(channel_url, websocket=websocket)

                # await YtVideoInfo.get_channel_all_videos_info(
                #     all_playlist,
                #     output_folder=DOWNLOAD_PATH,
                #     subtitle_langs="en,zh,zh-Hant"
                # )

                # 插入資料到MongoDB
                await yt_collection_manager.insert_document_mongdb(
                    mongoDBCtrl=MONGODB,
                    collection='yt_channel_playlist_collection',
                    document={
                        "from": 'python_st_server',
                        "dt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "providerName": providerName,
                        "channelCategory": courseCategory,
                        "channelName": courseName,
                        "channelContent": courseContent,
                        "channel_url": channel_url,
                        "data": all_playlist
                    }
                )

                await run_in_threadpool(logging.info, f"Done....")

                # # Close the WebSocket connection after processing is complete
                # await websocket.close()
                # break

        except WebSocketDisconnect:
            break


if __name__ == "__main__":
    if RUN.find('local') != -1:
        uvicorn.run('server_st:app', host="0.0.0.0", port=DEPLOY_PORT, workers=1)
