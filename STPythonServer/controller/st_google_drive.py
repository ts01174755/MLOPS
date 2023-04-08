import numpy as np
import re
import pandas as pd
from src.my_model.mongodb import MongoDB
from src.my_model.postgres import PostgresDB
from src.my_model.line import LineNotify
from datetime import datetime, timedelta
import time

def extract_datetime(text):
    """Extract datetime from text"""
    match = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', text)
    if match:
        return match.group()
    else:
        return None

class STGoogleDrive():

    def __init__(self):
        pass

    def searchPostgres(self, PROGRESDB_INFO):
        postgres = PostgresDB(
            user=PROGRESDB_INFO["POSTGRES_USER"],
            password=PROGRESDB_INFO["POSTGRES_PASSWORD"],
            host=PROGRESDB_INFO["POSTGRES_HOST"],
            port=PROGRESDB_INFO["POSTGRES_PORT"],
            database=PROGRESDB_INFO["POSTGRES_DATABASE"],
        )
        # 連接儲存解析後的DataBase
        conn = postgres.connect()
        # conn = postgres.connectSQLAlchemy()
        query = PROGRESDB_INFO["QUERY_SQL"].replace('"', "'")

        # 撈取資料
        df = pd.read_sql(query, conn)
        return df

    def fileMoveAndCopy(self, googleDrive, data):
        notifyInfo = set()
        files = googleDrive.execute_shell_command(f'ls /Meet\ Recordings', print_file=False) # 查詢根目錄下所有檔案
        for f_ in files:
            record_datetime_str = extract_datetime(f_)
            if record_datetime_str is None: continue

            record_datetime = datetime.strptime(record_datetime_str, '%Y-%m-%d %H:%M')
            for data_ in data:
                course_start_time = data_[1]
                course_start = datetime.strptime(course_start_time, '%Y-%m-%d %H:%M')
                if (timedelta(minutes=-10) <= record_datetime - course_start) & (record_datetime - course_start < timedelta(minutes=10)):
                    fileName = f_.replace(' ', '\ ')
                    folderName1 = data_[6].replace(' ', '\ ')
                    folderName2 = data_[7].replace(' ', '\ ')
                    course_start = datetime.strftime(record_datetime, '%Y-%m-%d %H:%M').replace(' ', '\ ')
                    notifyInfo.add((folderName1, folderName2))

                    googleDrive.execute_shell_command(f"mkdir /Meet\ Recordings/原始檔案/{folderName1}/{folderName2}", print_file=False)
                    googleDrive.execute_shell_command(f"mkdir /Meet\ Recordings/暫存檔案/{folderName1}/{folderName2}", print_file=False)
                    googleDrive.execute_shell_command(f"cp /Meet\ Recordings/{fileName} /Meet\ Recordings/暫存檔案/{folderName1}/{folderName2}/{folderName1}_{folderName2}_{course_start}", print_file=False)
                    googleDrive.execute_shell_command(f"mv /Meet\ Recordings/{fileName} /Meet\ Recordings/原始檔案/{folderName1}/{folderName2}/{folderName1}_{folderName2}_{course_start}", print_file=False)

        return notifyInfo

    def postLineNotify(self, token, message):
        # 取得 token

        lineNotify = LineNotify(token)
        lineNotify.send(message)

        return 'success'

if __name__ == '__main__':
    pass