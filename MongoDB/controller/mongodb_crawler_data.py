import requests
from src.my_model.mongodb import MongoDB
import subprocess


class CrawlerData:
    def __init__(self):
        pass

    def get_crawlerdata_to_mongodb(
        self, URL, COOKIES, MONGODB_INFO, COLLECTION, DATATIME
    ):
        # 獲取網頁回應
        crawlerRes = requests.get(URL, cookies=COOKIES)

        # 獲取 mongodb 資訊
        mongoDB = MongoDB(
            user_name=MONGODB_INFO["MONGODB_USER"],
            user_password=MONGODB_INFO["MONGODB_PASSWORD"],
            host=MONGODB_INFO["MONGODB_HOST"],
            port=MONGODB_INFO["MONGODB_PORT"],
            database_name=MONGODB_INFO["MONGODB_DATABASE"],
        )

        # 獲取 mongodb 資料
        mongoDB.insert_document(
            COLLECTION,
            document={
                "URL": URL,
                "dt": DATATIME,
                "crawlerResText": crawlerRes.text,
            },
        )
        return "success"

    def get_crawlerZipFile_to_fileSystem(self, URL, FILEPATH):
        # 獲取網頁回應
        crawlerRes = requests.get(URL, allow_redirects=True)
        open(FILEPATH, "wb").write(crawlerRes.content)

        # 解壓縮
        subprocess.run(
            f"unzip -o {FILEPATH} -d {'/'.join(FILEPATH.split('/')[:-1])}", shell=True
        )

        # 刪除壓縮檔
        subprocess.run(f"rm {FILEPATH}", shell=True)
        return "success"
