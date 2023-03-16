import os;import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.PostgresCtrl import PostgresCtrl
from FS_PythonServer.package.LineNotifyServer import LineNotifyServer
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import time


if __name__ == '__main__':
    print('2_lineNotifyServer.py')

    # 每日執行 - 爬蟲
    load_dotenv(find_dotenv('env/.env'))
    lineNotifyServer = MLFlow(LineNotifyServer())

    TABLE = 'google_form' # 這是正式用的table
    TODAY = time.localtime(time.time() + 8 * 60 * 60) # 時間校準
    rows = lineNotifyServer.searchPostgres(
        postgresCtrl = PostgresCtrl(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='originaldb'
        ),
        query = f'SELECT * FROM {TABLE} WHERE dt < \'{time.strftime("%Y-%m-%d", TODAY)}\''
    )
    print(rows)
