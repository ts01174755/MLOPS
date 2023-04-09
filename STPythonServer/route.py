import os
import sys
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from controller.st_google_drive import STGoogleDrive
from controller.st_line_notify import STLineNotify
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import st_server_config as config
import json
app = FastAPI()


class STCrawlerRequestBody(BaseModel):
    DEFAULT_DICT: dict = {}


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}

@app.get("/stPythonServer/stGoogleDrive")
def st_google_drive_get():
    return {"message": "here is stPythonServer/stGoogleDrive"}

@app.post("/stPythonServer/stGoogleDrive")
def st_google_drive(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    # 每日執行 - 爬蟲
    st_google_drive = STGoogleDrive()
    df = st_google_drive.searchPostgres(
        # MONGODB_INFO=params.DEFAULT_DICT['MONGODB_INFO'],
        PROGRESDB_INFO=params.DEFAULT_DICT['PROGRESDB_INFO'],
    )

    # 撰寫 googleDrive 模擬cd, rm, mkdir, 等shell操作
    notifyInfo = st_google_drive.fileMoveAndCopy(
        GOOGLE_DRIVE_INFO=params.DEFAULT_DICT['GOOGLE_DRIVE_INFO'],
        df = df
    )

    line_message = st_google_drive.line_notify_message(notifyInfo)

    with open(params.DEFAULT_DICT['NOTIFY_TOKEN_FILE'], 'r') as f:
        lineNotifyToken = json.load(f)

    st_line_notify = STLineNotify()
    st_line_notify.postLineNotify(
        token = lineNotifyToken[params.DEFAULT_DICT['NOTIFY_TOKEN_TYPE']],
        message = line_message
    )

    return {"message": 'success'}



# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.ST_PYSERVER_PORT)
