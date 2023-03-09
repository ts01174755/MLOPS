import os; import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from package.common.DatabaseCtrl import MongoDBCtrl
from DE_MongoDB.package.STCrawler import STCrawler
from dotenv import load_dotenv, find_dotenv
import time
from datetime import datetime

if __name__ == '__main__':
    print('Here is MongoCrwaler')

    # 環境變數
    load_dotenv(find_dotenv('env/.env'))
    URL = os.getenv('ST_ALLURL')
    cookies = {'ST': os.getenv('ST_TOKEN')}

    # 爬蟲
    stCrawler = MLFlow(STCrawler())
    crawlerResText = stCrawler.get_st_all_data(
        URL=URL,
        cookies=cookies
    )

    # 連接MongoDB與寫入資料
    load_dotenv(find_dotenv('env/.env'))
    mongodb = MLFlow(MongoDBCtrl(
        user_name=os.getenv('MongoDB_USER'),
        user_password=os.getenv('MongoDB_PASSWORD'),
        host=os.getenv('MongoDB_HOST'),
        port=int(os.getenv('MongoDB_PORT')),
        database_name='originaldb'
    ))
    now = time.localtime(time.time() + 8 * 60 * 60) # 時間校準
    mongodb.insert_document('st_all_data', {"URL": URL, "dt": time.strftime("%Y-%m-%d %H:%M:%S", now), "crawlerResText": crawlerResText})

