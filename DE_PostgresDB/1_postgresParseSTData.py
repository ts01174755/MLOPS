import os;import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.MongoDBCtrl import MongoDBCtrl
from package.controller.PostgresCtrl import PostgresCtrl
from DE_PostgresDB.package.PostgresParseSTData import PostgresParseSTData
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import time

if __name__ == '__main__':
    load_dotenv(find_dotenv('env/.env'))
    TODAY = time.localtime(time.time() + 8 * 60 * 60) # 時間校準
    TOMORROW = time.localtime(time.time() + 8 * 60 * 60 + 24 * 60 * 60) # 時間校準
    # TABLE = 'temptb' # 這是測試用的table
    TABLE = 'st_all_data' # 這是正式用的table

    # 每日執行 - 爬蟲
    postgresParseSTData = MLFlow(PostgresParseSTData())
    stData = postgresParseSTData.parseSTData(
        mongoDBCtrl = MongoDBCtrl(
            user_name=os.getenv('MongoDB_USER'),
            user_password=os.getenv('MongoDB_PASSWORD'),
            # host=os.getenv('MongoDB_HOST'), # 這個是用來連接外部的MongoDB(外部連接)
            host='mongodb',     # docker-compose.yml中的service name(在docker container中連接)
            port=int(os.getenv('MongoDB_PORT')),
            database_name='originaldb'
        ),
        collection = 'st_all_data',
        queryFilter = {
            "dt": {
                "$gte": time.strftime("%Y-%m-%d", TODAY),
                "$lt": time.strftime("%Y-%m-%d", TOMORROW)
            }
        }
    )

    # 連接PostgresDB與寫入資料
    postgresParseSTData.insertSTData(
        postgresCtrl = PostgresCtrl(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='originaldb'
        ),
        table = TABLE,
        dataList = stData,
        dt = time.strftime("%Y-%m-%d %H:%M:%S", TODAY)
    )

    # 建立資料表的schema說明
    postgresParseSTData.makeInsertSTDataSchema(
        postgresCtrl=PostgresCtrl(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='originaldb'
        ),
        tableName=TABLE,
        schemaDict={
            'dt': '資料更新時間',
            'memo': 'ST所有課程資料',
            'commondata1': '"AdminCourses"',
            'uniquechar1': '開始時間',
            'uniquechar2': '結束時間',
            'uniquechar3': '所屬單位',
            'uniquechar4': '上課地點',
            'uniquechar5': '年級',
            'uniquechar6': '課程',
            'uniquechar7': '老師',
            'uniquechar8': '學生'
        },
        schemaFilePath='DE_PostgresDB/file/STAllDataSchema.csv',
        columnList=[
            'dt', 'memo', 'commondata1', 'commondata2', 'commondata3', 'commondata4', 'commondata5',
            'commondata6', 'commondata7', 'commondata8', 'commondata9', 'commondata10', 'uniquechar1',
            'uniquechar2', 'uniquechar3', 'uniquechar4', 'uniquechar5', 'uniquechar6', 'uniquechar7',
            'uniquechar8', 'uniquechar9', 'uniquechar10', 'uniqueint1', 'uniqueint2', 'uniqueint3',
            'uniqueint4', 'uniqueint5', 'uniqueint6', 'uniqueint7', 'uniqueint8', 'uniqueint9',
            'uniqueint10', 'uniquefloat1', 'uniquefloat2', 'uniquefloat3', 'uniquefloat4', 'uniquefloat5',
            'uniquefloat6', 'uniquefloat7', 'uniquefloat8', 'uniquefloat9', 'uniquefloat10', 'uniquefloat11',
            'uniquefloat12', 'uniquefloat13', 'uniquefloat14', 'uniquefloat15', 'uniquestring1',
            'uniquestring2', 'uniquestring3', 'uniquestring4', 'uniquestring5', 'uniquejason'
        ]
    )


    # # 指定執行日期範圍
    # today = datetime(2023, 3, 9, 0, 0, 0)
    # while today < datetime(2023, 3, 11, 0, 0, 0):
    #     ...
    #     today = today + timedelta(days=1)