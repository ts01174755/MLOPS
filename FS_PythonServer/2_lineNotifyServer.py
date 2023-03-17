import os;import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.PostgresCtrl import PostgresCtrl
from FS_PythonServer.package.LineNotifyServer import LineNotifyServer
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import time
import json

if __name__ == '__main__':
    print('2_lineNotifyServer.py')

    # 每日執行 - 爬蟲
    load_dotenv(find_dotenv('env/.env'))
    lineNotifyServer = MLFlow(LineNotifyServer())

    TABLE = 'google_form' # 這是正式用的table
    YESTERDAY = time.localtime(time.time() + 8 * 60 * 60 - 24 * 60 * 60) # 時間校準
    rows = lineNotifyServer.searchPostgres(
        postgresCtrl = PostgresCtrl(
            # host=os.getenv('POSTGRES_HOST'),
            host='postgres15.2',
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='originaldb'
        ),
        query = f'\
            SELECT \
                uniquechar1,uniquechar2,uniquechar3,uniquechar4,uniquechar5,\
                uniquechar6,uniquechar7,uniquechar8 \
            FROM original.{TABLE} WHERE uniquechar1 >= \'{time.strftime("%Y%m%d", YESTERDAY)}\';'
    )
    print(rows)

    with open('env/LineNotify.json', 'r') as f: lineNotifyToken = json.load(f)
    for row_ in rows:
        lineNotifyServer.postLineNotify(
            token = lineNotifyToken['雲課堂 - AI助手'],
            message =
            f'\n您好，想在這裡跟您註冊新課程，供老師打卡使用，以下是註冊資訊：'
            f'\n填表日:{row_[0]}\n申請人:{row_[1]}\n所屬單位:{row_[2]}\n上課地點:{row_[3]}\n'
            f'年級:{row_[4]}\n課程:{row_[5]}\n老師:{row_[6]}\n學生:{row_[7]}'
        )
        time.sleep(1)
