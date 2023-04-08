import os
import sys
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from controller.st_google_drive import STGoogleDrive
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import st_server_config as config

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
    rows = st_google_drive.searchPostgres(
        # MONGODB_INFO=params.DEFAULT_DICT['MONGODB_INFO'],
        PROGRESDB_INFO=params.DEFAULT_DICT['PROGRESDB_INFO'],
    )
    return rows
    # # 撰寫 googleDrive 模擬cd, rm, mkdir, 等shell操作
    # notifyInfo = stGoogleDrive.fileMoveAndCopy(
    #     googleDrive = GoogleDrive(
    #         TOKEN='env/googleDriveToken_stpeteamshare.json',
    #         CLIENT_SECRET_FILE='env/client_secret_stpeteamshare.json',
    #         SCOPES=['https://www.googleapis.com/auth/drive'],  # 讀寫權限，刪除client_secret.json後，重新執行程式，會要求重新授權
    #         # SCOPES=['https://www.googleapis.com/auth/drive.metadata.readonly'] # 只有讀取權限，刪除client_secret.json後，重新執行程式，會要求重新授權
    #     ),
    #     data = rows
    # )
    #
    #
    # with open('env/LineNotify.json', 'r') as f: lineNotifyToken = json.load(f)
    # for info_ in notifyInfo:
    #     stGoogleDrive.postLineNotify(
    #         token = lineNotifyToken['雲課堂 - 網課群'],
    #         message =f'\n {info_[1]}老師，您的課程「{info_[0]}」影片已經備份，上課辛苦了。'
    #     )
    #     time.sleep(1)



# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.ST_PYSERVER_PORT)
