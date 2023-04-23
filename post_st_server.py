import os
import sys
import time
from dotenv import load_dotenv, find_dotenv
import subprocess
import json

load_dotenv(find_dotenv("env/.env"))

if __name__ == "__main__":
    # 執行環境
    RUN = "st_google_drive" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "st_google_drive":
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        DATA_TOMORROW = time.strftime(
            "%Y-%m-%d", time.localtime(time.time() + 24 * 60 * 60)
        )
        PROGRESDB_SCHEMA = "original"
        PROGRESDB_TABLE = ["st_all_data", "google_form", "tempdb"][0]

        # ---------------------- route: postgresParseMongodb -----------------------
        QUERY_SQL = f'\
        SELECT \
            dt, uniquechar1, uniquechar2, uniquechar3, uniquechar4, \
            uniquechar5, uniquechar6, uniquechar7, uniquechar8 \
            FROM {PROGRESDB_SCHEMA}.{PROGRESDB_TABLE} \
            WHERE 1=1 \
                AND dt >= "{DATA_DAY}" AND dt < "{DATA_TOMORROW}" \
                AND uniquechar3 = "雲課堂" \
                AND uniquechar7 = "羅苡心 Xinn"\
            ORDER BY uniquechar1 DESC;'
        POST_INFO = {
            "DEFAULT_DICT": {
                "DATA_DAY": DATA_DAY,
                "GOOGLE_DRIVE_INFO": {
                    "TOKEN": 'env/googleDriveToken_stpeteamshare.json',
                    "CLIENT_SECRET_FILE": 'env/client_secret_stpeteamshare.json',
                    "SCOPES": ['https://www.googleapis.com/auth/drive'],
                },
                "NOTIFY_TOKEN_FILE": 'env/LineNotify.json',
                "NOTIFY_TOKEN_TYPE": ['私人Notify', '雲課堂 - Hana'][0],
                "PROGRESDB_SCHEMA": PROGRESDB_SCHEMA,
                "PROGRESDB_TABLE": PROGRESDB_TABLE,
                "PROGRESDB_SCHEMA_DICT": {
                    "dt": "資料更新時間",
                    "memo": "新申請課程",
                    "commondata1": '"GoogleForm表單"',
                    "uniquechar1": "填表日",
                    "uniquechar2": "申請人(Email)",
                    "uniquechar3": "所屬單位",
                    "uniquechar4": "上課地點",
                    "uniquechar5": "年級",
                    "uniquechar6": "課程",
                    "uniquechar7": "老師",
                    "uniquechar8": "學生",
                },
                "QUERY_SQL": QUERY_SQL
            }
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8003/stPythonServer/stGoogleDrive"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8003/stPythonServer/stGoogleDrive",
            shell=True,
        )
