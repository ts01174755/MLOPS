import os
import sys
import time
from dotenv import load_dotenv, find_dotenv
import subprocess
import json
load_dotenv(find_dotenv("env/.env"))

if __name__ == "__main__":

    RUN = "google_form" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "st_crawler":
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())

        # ---------------------- route: st_crawler -----------------------
        ST_CRAWLER_DATA = {
            "DATA_TIME": DATA_TIME,
            "URL": os.getenv("ST_ALLURL"),
            "COOKIES": {"ST": os.getenv("ST_TOKEN")},
            "COLLECTION": ["st_all_data", "tempdb", "google_form"][0],
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(ST_CRAWLER_DATA)}' http://localhost:8001/MongoDB/crawlerDataPost"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(ST_CRAWLER_DATA)}' http://localhost:8001/MongoDB/crawlerDataPost",
            shell=True,
        )

    elif RUN == "google_form":
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        GOOGLEFORM_DATA = {
            "DATA_TIME": DATA_TIME,
            "TOKEN": f"env/token.json",
            "CLIENT_SECRET_FILE": f"env/client_secret.json",
            "SCOPES": "https://www.googleapis.com/auth/forms.responses.readonly",
            "FORMID": "1sqxcABwDaVFyGD1cTo0-O0BoJIGWJccioaXGkxKMZv8",
            "DISCOVERY_DOC": "https://forms.googleapis.com/$discovery/rest?version=v1",
            "COLLECTION": ["st_all_data", "tempdb", "google_form"][2],
            # "COLLECTION": COLLECTION_TEMPDB,
        }

        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(GOOGLEFORM_DATA)}' http://localhost:8001/MongoDB/googleFormDataPost"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(GOOGLEFORM_DATA)}' http://localhost:8001/MongoDB/googleFormDataPost",
            shell=True,
        )
        time.sleep(5)

    elif RUN == "futuresExchange":
        # 從五天前的日期開始執行
        for i in range(0, -1, -1):
            DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            DATA_DAY = time.strftime("%Y_%m_%d", time.localtime(time.time() - 86400 * i))
            FILE_NAME = f"Daily_{DATA_DAY}.zip"
            FUTURES_EXCHANGE_DATA = {
                "URL": f"https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/{FILE_NAME}",  # 下載檔案的網址
                "FILENAME": f"{FILE_NAME.split('.')[0]}",  # 下載檔案的路徑
            }

            print(
                f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(FUTURES_EXCHANGE_DATA)}' http://localhost:8001/MongoDB/crawlerZipFilePost"
            )
            subprocess.run(
                f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(FUTURES_EXCHANGE_DATA)}' http://localhost:8001/MongoDB/crawlerZipFilePost",
                shell=True,
            )
