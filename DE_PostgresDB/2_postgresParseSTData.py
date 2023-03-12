import os;
import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from DE_PostgresDB.package.PostgresParseSTData import PostgresParseSTData
from package.controller.PostgresCtrl import PostgresCtrl
from package.controller.MongoDBCtrl import MongoDBCtrl
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import time

if __name__ == '__main__':
    load_dotenv(find_dotenv('env/.env'))
    TODAY = time.localtime(time.time() + 8 * 60 * 60) # 時間校準
    TOMORROW = time.localtime(time.time() + 8 * 60 * 60 + 24 * 60 * 60) # 時間校準
    TABLE = 'temptb' # 這是測試用的table
    # TABLE = 'st_all_data' # 這是正式用的table

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

    # # 指定執行日期範圍
    # today = datetime(2023, 3, 9, 0, 0, 0)
    # while today < datetime(2023, 3, 11, 0, 0, 0):
    #     ...
    #     today = today + timedelta(days=1)