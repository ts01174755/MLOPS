import requests
import subprocess


class CrawlerData:
    def __init__(self):
        pass

    def get_crawlerdata_to_mongodb(
        self, URL, COOKIES, Mongodb, COLLECTION, DATATIME
    ):
        # 獲取網頁回應
        crawlerRes = requests.get(URL, cookies=COOKIES)
        # 獲取 mongodb 資料
        Mongodb.insert_document(
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
        with open(FILEPATH, "wb") as f:
            f.write(crawlerRes.content)

        # 解壓縮
        subprocess.run(
            f"unzip -o {FILEPATH} -d {'/'.join(FILEPATH.split('/')[:-1])}", shell=True
        )

        # 刪除壓縮檔
        subprocess.run(f"rm {FILEPATH}", shell=True)
        return "success"
