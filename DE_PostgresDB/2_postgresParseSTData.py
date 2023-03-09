import os; import sys;
if len(sys.argv) > 1:
    print(sys.argv[1])
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from package.common.DatabaseCtrl import PostgresCtrl, MongoDBCtrl
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import time

if __name__ == '__main__':
    # 連接儲存爬蟲DataBase
    load_dotenv(find_dotenv('env/.env'))
    mongodb = MLFlow(MongoDBCtrl(
        user_name=os.getenv('MongoDB_USER'),
        user_password=os.getenv('MongoDB_PASSWORD'),
        # host=os.getenv('MongoDB_HOST'), # 這個是用來連接外部的MongoDB(外部連接)
        host='mongodb',     # docker-compose.yml中的service name(在docker container中連接)
        port=int(os.getenv('MongoDB_PORT')),
        database_name='originaldb'
    ))
    # 取得當天的年
    year = datetime.today().strftime('%Y')
    # 取得當天的月
    month = datetime.today().strftime('%m')
    # 取得當天的日
    day = datetime.today().strftime('%d')
    nowOfStart = datetime(int(year), int(month), int(day), 0, 0, 0)

    # mongodb查詢一段時間內的資料
    now = time.localtime(time.time() + 8 * 60 * 60) # 時間校準
    rows = mongodb.find_document(
        'st_all_data', {"dt": {"$gte": str(nowOfStart)}}
        , limit=10
    )
    print(rows)