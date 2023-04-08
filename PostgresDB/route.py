import os
import sys

os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from controller.postgres_parse_mongodb_data import PosgresParseMongodbData
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import progresdb_config as config

app = FastAPI()


class STCrawlerRequestBody(BaseModel):
    DATA_TIME: str = None
    MONGODB_INFO: dict = None
    PROGRESDB_INFO: dict = None


# 部署測試服務
@app.get("/")
def get_hello_message():
    return {"message": "Hello World"}


@app.post("/PostgresDB/mongodbToProgres/stCreateCourseForm")
def st_create_course_form(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    COLUMNS_LIST = [
        "dt",
        "memo",
        "commondata1",
        "commondata2",
        "commondata3",
        "commondata4",
        "commondata5",
        "commondata6",
        "commondata7",
        "commondata8",
        "commondata9",
        "commondata10",
        "uniquechar1",
        "uniquechar2",
        "uniquechar3",
        "uniquechar4",
        "uniquechar5",
        "uniquechar6",
        "uniquechar7",
        "uniquechar8",
        "uniquechar9",
        "uniquechar10",
        "uniqueint1",
        "uniqueint2",
        "uniqueint3",
        "uniqueint4",
        "uniqueint5",
        "uniqueint6",
        "uniqueint7",
        "uniqueint8",
        "uniqueint9",
        "uniqueint10",
        "uniquefloat1",
        "uniquefloat2",
        "uniquefloat3",
        "uniquefloat4",
        "uniquefloat5",
        "uniquefloat6",
        "uniquefloat7",
        "uniquefloat8",
        "uniquefloat9",
        "uniquefloat10",
        "uniquefloat11",
        "uniquefloat12",
        "uniquefloat13",
        "uniquefloat14",
        "uniquefloat15",
        "uniquestring1",
        "uniquestring2",
        "uniquestring3",
        "uniquestring4",
        "uniquestring5",
        "uniquejason",
    ]
    # 每日執行 - 爬蟲
    posgresParseMongodbData = PosgresParseMongodbData()
    googleFormDF = posgresParseMongodbData.parseGoogleSTFromData(
        MONGODB_INFO=params.MONGODB_INFO,
        PROGRESDB_INFO=params.PROGRESDB_INFO,
        DATA_TIME=params.DATA_TIME,
        columnList=COLUMNS_LIST
    )

    # 連接PostgresDB與寫入資料
    posgresParseMongodbData.insertPostgresData(
        PROGRESDB_INFO=params.PROGRESDB_INFO,
        dataFrame=googleFormDF,
    )

    # 建立資料表的schema說明
    posgresParseMongodbData.makeInsertGoogleFromDataSchema(
        PROGRESDB_INFO=params.PROGRESDB_INFO,
        tableName=params.PROGRESDB_INFO["PROGRESDB_TABLE"],
        schemaDict=params.PROGRESDB_INFO["PROGRESDB_SCHEMA_DICT"],
        schemaFilePath=params.PROGRESDB_INFO["PROGRESDB_SCHEMA_FILE_PATH"],
        columnList=COLUMNS_LIST,
    )
    return {"message": "insert success"}


@app.post("/PostgresDB/mongodbToProgres/stAdminCourses")
def st_admin_course(params: STCrawlerRequestBody = STCrawlerRequestBody()):
    COLUMNS_LIST = [
        "dt",
        "memo",
        "commondata1",
        "commondata2",
        "commondata3",
        "commondata4",
        "commondata5",
        "commondata6",
        "commondata7",
        "commondata8",
        "commondata9",
        "commondata10",
        "uniquechar1",
        "uniquechar2",
        "uniquechar3",
        "uniquechar4",
        "uniquechar5",
        "uniquechar6",
        "uniquechar7",
        "uniquechar8",
        "uniquechar9",
        "uniquechar10",
        "uniqueint1",
        "uniqueint2",
        "uniqueint3",
        "uniqueint4",
        "uniqueint5",
        "uniqueint6",
        "uniqueint7",
        "uniqueint8",
        "uniqueint9",
        "uniqueint10",
        "uniquefloat1",
        "uniquefloat2",
        "uniquefloat3",
        "uniquefloat4",
        "uniquefloat5",
        "uniquefloat6",
        "uniquefloat7",
        "uniquefloat8",
        "uniquefloat9",
        "uniquefloat10",
        "uniquefloat11",
        "uniquefloat12",
        "uniquefloat13",
        "uniquefloat14",
        "uniquefloat15",
        "uniquestring1",
        "uniquestring2",
        "uniquestring3",
        "uniquestring4",
        "uniquestring5",
        "uniquejason",
    ]
    # 每日執行 - 爬蟲
    posgresParseMongodbData = PosgresParseMongodbData()
    googleFormDF = posgresParseMongodbData.parseSTData(
        MONGODB_INFO=params.MONGODB_INFO,
        PROGRESDB_INFO=params.PROGRESDB_INFO,
        DATA_TIME=params.DATA_TIME,
    )

    # 連接PostgresDB與寫入資料
    posgresParseMongodbData.insertPostgresData(
        PROGRESDB_INFO=params.PROGRESDB_INFO,
        dataFrame=googleFormDF,
    )

    # 建立資料表的schema說明
    posgresParseMongodbData.makeInsertGoogleFromDataSchema(
        PROGRESDB_INFO=params.PROGRESDB_INFO,
        tableName=params.PROGRESDB_INFO["PROGRESDB_TABLE"],
        schemaDict=params.PROGRESDB_INFO["PROGRESDB_SCHEMA_DICT"],
        schemaFilePath=params.PROGRESDB_INFO["PROGRESDB_SCHEMA_FILE_PATH"],
        columnList=COLUMNS_LIST,
    )
    return {"message": "insert success"}


# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.PROGRESDB_PYSERVER_PORT)
