import os
import sys

os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from controller.mongodb_crawler_data import CrawlerData
from controller.mongodb_googleform_data import GoogleFormData
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import mongodb_config as config

app = FastAPI()


class STCrawlerRequestBody(BaseModel):
    DATA_TIME: str = None
    URL: str = None
    COOKIES: dict = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None
    MONGODB_PORT: int = None
    MONGODB_HOST: str = None
    MONGODB_DATABASE: str = None
    COLLECTION: str = None


class CrawlerFileRequestBody(BaseModel):
    URL: str = None
    FILEPATH: str = None


class GoogleFormDataRequestBody(BaseModel):
    DATA_TIME: str = None
    TOKEN: str = None
    CLIENT_SECRET_FILE: str = None
    SCOPES: str = None
    FORMID: str = None
    DISCOVERY_DOC: str = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None
    MONGODB_PORT: int = None
    MONGODB_HOST: str = None
    MONGODB_DATABASE: str = None
    COLLECTION: str = None


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.post("/MongoDB/crawlerDataPost")
def crawler_data_post(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    crawler_data = CrawlerData()

    # 爬蟲
    crawler_data.get_crawlerdata_to_mongodb(
        URL=params.URL,
        COOKIES=params.COOKIES,
        MONGODB_INFO={
            "MONGODB_USER": params.MONGODB_USER,
            "MONGODB_PASSWORD": params.MONGODB_PASSWORD,
            "MONGODB_HOST": params.MONGODB_HOST,
            "MONGODB_PORT": params.MONGODB_PORT,
            "MONGODB_DATABASE": params.MONGODB_DATABASE,
        },
        COLLECTION=params.COLLECTION,
        DATATIME=params.DATA_TIME,
    )
    return {"message": "insert success"}


@app.post("/MongoDB/crawlerZipFilePost")
def crawler_zip_file_post(params: CrawlerFileRequestBody = CrawlerFileRequestBody()):
    crawler_data = CrawlerData()

    # 爬蟲
    crawler_data.get_crawlerZipFile_to_fileSystem(
        URL=params.URL,
        FILEPATH=params.FILEPATH,
    )
    return {"message": "insert success"}


@app.post("/MongoDB/googleFormDataPost")
def google_form_data_post(
    params: GoogleFormDataRequestBody = GoogleFormDataRequestBody(),
):
    google_form_data = GoogleFormData()

    google_form_data.get_googleformdata_to_mongodb(
        TOKEN=params.TOKEN,
        CLIENT_SECRET_FILE=params.CLIENT_SECRET_FILE,
        SCOPES=params.SCOPES,
        DISCOVERY_DOC=params.DISCOVERY_DOC,
        MONGODB_INFO={
            "MONGODB_USER": params.MONGODB_USER,
            "MONGODB_PASSWORD": params.MONGODB_PASSWORD,
            "MONGODB_HOST": params.MONGODB_HOST,
            "MONGODB_PORT": params.MONGODB_PORT,
            "MONGODB_DATABASE": params.MONGODB_DATABASE,
        },
        COLLECTION=params.COLLECTION,
        FORMID=params.FORMID,
        DATATIME=params.DATA_TIME,
    )
    return {"message": "insert success"}


# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.MONGODB_PYSERVER_PORT)
