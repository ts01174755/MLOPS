import os;
import re
import sys;
if len(sys.argv) > 1:
    print(sys.argv[1])
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from package.common.DatabaseCtrl import PostgresCtrl, MongoDBCtrl
from package.common.BS4Crawler import bs4Crawler
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import time

class PostgresParseSTData():

    def __init__(self):
        pass

    @classmethod
    def parseSTData(cls):
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
        rows = mongodb.find_document(
            'st_all_data', {"dt": {"$gte": str(nowOfStart)}}
        )
        crawlerResText = rows[-1]['crawlerResText']
        reStr = re.search(r'events: \[\n\n\{.*\},    \]', crawlerResText).group(0)
        reStr = reStr.replace('events: [\n\n', '').replace(',    ]', '')
        reStrList = reStr.split('},{')

        # 連接儲存解析後的DataBase
        crawlerDataList = []
        for reStr in reStrList:
            crawlerData = []
            reStr = reStr.replace('{', '').replace('}', '').replace('title:', '').replace('start:', '').replace('end:', '')
            reStrs = reStr.split(',')

            crawlerData.append(reStrs[-2])
            crawlerData.append(reStrs[-1])
            reStrDataList = reStrs[0].replace("\'", "").split('\t')
            crawlerData.append(reStrDataList[0].replace('所屬單位：', ''))
            crawlerData.append(reStrDataList[1].replace('上課地點：', ''))
            crawlerData.append(reStrDataList[2].replace('年級：', ''))
            crawlerData.append(reStrDataList[3].replace('課程：', ''))
            crawlerData.append(reStrDataList[4].replace('老師：', ''))
            crawlerData.append(reStrDataList[5].replace('學生：', ''))
            crawlerData.append(reStrDataList[6].replace('上課日期：', ''))
            crawlerData.append(reStrDataList[7].replace('開始時間：', ''))
            crawlerData.append(reStrDataList[8].replace('結束時間：', ''))

            crawlerDataList.append(crawlerData)
        print(crawlerDataList)

        return crawlerDataList

