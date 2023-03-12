import os; import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.MongoDBCtrl import MongoDBCtrl
from DE_MongoDB.package.STCrawler import STCrawler
from dotenv import load_dotenv, find_dotenv
import time

if __name__ == '__main__':
    load_dotenv(find_dotenv('env/.env'))
    # COLLECTION = 'tempdb'   # 這邊是為了測試，所以先存入 tempdb，之後再改成正式的資料庫
    COLLECTION = 'st_all_data'  # 這邊是正式的資料庫

    # 每日解析爬蟲資料
    stCrawler = MLFlow(STCrawler())
    crawlerResText = stCrawler.get_st_all_data(
        URL=os.getenv('ST_ALLURL'),
        cookies={'ST': os.getenv('ST_TOKEN')}
    )

    # 將爬蟲資料存入MongoDB
    stCrawler.mongodb_insert_document(
        mongoDBCtrl=MongoDBCtrl(
            user_name=os.getenv('MongoDB_USER'),
            user_password=os.getenv('MongoDB_PASSWORD'),
            host=os.getenv('MongoDB_HOST'),
            port=int(os.getenv('MongoDB_PORT')),
            database_name='originaldb'
        ),
        collection=COLLECTION,
        document={
            "URL": os.getenv('ST_ALLURL'),
            "dt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 8 * 60 * 60)),
            "crawlerResText": crawlerResText
        }
    )
