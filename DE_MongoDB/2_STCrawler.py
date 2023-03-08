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


if __name__ == '__main__':
    print('Here is MongoCrwaler')

    # 爬蟲
    cookies = {'ST': 'WPU199208090986389515'}
    URL = 'http://roma254-1.kddns.info:8022/Course/AdminCourses.php'
    stCrawler = MLFlow(STCrawler())
    crawlerResText = stCrawler.get_st_all_data(URL, cookies=cookies)
    # print(crawlerResText)

    # 連接MongoDB
    load_dotenv(find_dotenv('env/.env'))
    mongodb = MLFlow(MongoDBCtrl(
        user_name=os.getenv('MongoDB_USER'),
        user_password=os.getenv('MongoDB_PASSWORD'),
        host=os.getenv('MongoDB_HOST'),
        port=int(os.getenv('MongoDB_PORT')),
        database_name='originaldb'
    ))
    # 把time.time()轉成2021-09-01 00:00:00格式
    mongodb.insert_document('tempdb', {"URL": URL, "dt": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "crawlerResText": crawlerResText})

