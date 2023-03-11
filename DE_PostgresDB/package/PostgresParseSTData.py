import os;
import re
import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.controller.PostgresCtrl import PostgresCtrl
from package.controller.MongoDBCtrl import MongoDBCtrl
from dotenv import load_dotenv, find_dotenv


class PostgresParseSTData():

    def __init__(self):
        pass

    @classmethod
    def parseSTData(cls, dt1=None, dt2=None):
        # 連接儲存爬蟲DataBase
        load_dotenv(find_dotenv('env/.env'))
        mongodb = MongoDBCtrl(
            user_name=os.getenv('MongoDB_USER'),
            user_password=os.getenv('MongoDB_PASSWORD'),
            # host=os.getenv('MongoDB_HOST'), # 這個是用來連接外部的MongoDB(外部連接)
            host='mongodb',     # docker-compose.yml中的service name(在docker container中連接)
            port=int(os.getenv('MongoDB_PORT')),
            database_name='originaldb'
        )

        # mongodb查詢一段時間內的資料
        rows = mongodb.find_document(
            'st_all_data', {"dt": {"$gte": dt1, "$lt": dt2}},
        )
        crawlerResText = rows[-1]['crawlerResText']

        # 連接儲存解析後的DataBase
        reStr = re.search(r'events: \[\n\n\{.*\},    \]', crawlerResText).group(0)
        reStr = reStr.replace('events: [\n\n', '').replace(',    ]', '')
        reStrList = reStr.split('},{')
        crawlerDataList = []
        for reStr in reStrList:
            crawlerData = []
            reStr = reStr.replace('{', '').replace('}', '').replace('title:', '').replace('start:', '').replace('end:', '')
            reStrs = reStr.split(',')

            crawlerData.append(reStrs[-2].replace('\'', ''))
            crawlerData.append(reStrs[-1].replace('\'', ''))
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

        return crawlerDataList

    @classmethod
    def insertSTData(cls, DataList, now):
        # 連接儲存解析後的DataBase
        load_dotenv(find_dotenv('env/.env'))
        db = PostgresCtrl(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='originaldb'
        )
        db.connect()

        # 資料寫入 original.st_all_data
        for data_ in DataList:
            db.execute(f"\
            INSERT INTO original.st_all_data (\
                dt, memo, \
                commondata1, \
                uniquechar1, uniquechar2, uniquechar3, uniquechar4, uniquechar5, uniquechar6, uniquechar7, uniquechar8\
            ) \
            VALUES (\
                '{now}', 'ST所有課程資料', \
                'AdminCourses', \
                '{data_[0]}', '{data_[1]}', '{data_[2]}', '{data_[3]}', '{data_[4]}', '{data_[5]}', '{data_[6]}', '{data_[7]}'\
            );")  # 插入資料
        db.close()

