import numpy as np
import re
import pandas as pd
from src.my_model.mongodb import MongoDB
from src.my_model.postgres import PostgresDB
from src.my_model.google_drive import GoogleDrive
from datetime import datetime, timedelta
import time

def extract_datetime(text):
    """Extract datetime from text"""
    match = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', text)
    if match:
        return match.group()
    else:
        return None

def extract_classroom_code(text):
    """Extract classroom code from text"""
    match = re.search(r'(\w+-\w+-\w+)', text)
    if match:
        return match.group(1)
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
        conn = postgres.connectSQLAlchemy().connect()
        query = PROGRESDB_INFO["QUERY_SQL"].replace('"', "'")

        # 撈取資料
        df = pd.read_sql(postgres.getSQLText(query), conn)
        return df

    def fileMoveAndCopy(self, GOOGLE_DRIVE_INFO, df):
        # 連接Google Drive
        google_drive = GoogleDrive(
            TOKEN=GOOGLE_DRIVE_INFO['TOKEN'],
            CLIENT_SECRET_FILE=GOOGLE_DRIVE_INFO['CLIENT_SECRET_FILE'],
            SCOPES=GOOGLE_DRIVE_INFO['SCOPES']
        )

        # 搜索雲授課網課的錄製檔案
        COURSE_DELTA_MAX = timedelta(minutes=15)
        COURSE_DELTA_MIN = timedelta(minutes=-15)
        files = google_drive.execute_shell_command(f'ls /Meet\ Recordings', print_file=False) # 查詢根目錄下所有檔案
        data = df.to_numpy()
        classroom_Info = {}
        for f_ in files:
            classroom_code = extract_classroom_code(f_)
            if classroom_code is None: continue

            # 雲授課網課的開始時間
            for data_ in data:
                # 擷取雲授課網課的開始時間
                course_start_time = data_[1]
                course_start = datetime.strptime(course_start_time, '%Y-%m-%d %H:%M')

                # 擷取錄製檔案的時間
                record_datetime_str = extract_datetime(f_)
                record_datetime = datetime.strptime(record_datetime_str, '%Y-%m-%d %H:%M')

                # 錄製檔案的時間在雲授課網課的開始時間前後n分鐘內
                if (COURSE_DELTA_MIN <= record_datetime - course_start) & (record_datetime - course_start < COURSE_DELTA_MAX):
                    if classroom_code in classroom_Info:
                        classroom_Info[classroom_code].append({
                            '資料': data_,
                            '錄製檔案': f_
                        })
                    else:
                        classroom_Info[classroom_code] = [{
                            '資料': data_,
                            '錄製檔案': f_
                        }]

        notify_info = {}
        for code_ in classroom_Info.keys():
            # 比對資料"科目","老師"是否一樣，若不一樣，則跳過此循環
            flag = True
            for i in range(len(classroom_Info[code_])):
                if i == 0: continue
                if classroom_Info[code_][i]['資料'][6] != classroom_Info[code_][i-1]['資料'][6]:
                    flag = False
                    break
                if classroom_Info[code_][i]['資料'][7] != classroom_Info[code_][i-1]['資料'][7]:
                    flag = False
                    break
            if flag == False: continue

            # 整理notify_info
            subject_name = classroom_Info[code_][0]['資料'][6]
            teacher_name = classroom_Info[code_][0]['資料'][7]
            course_start_ = extract_datetime(classroom_Info[code_][0]['錄製檔案'])
            if teacher_name in notify_info:
                notify_info[teacher_name].append(f'{subject_name}_{teacher_name}_{course_start_}')
            else:
                notify_info[teacher_name] = [f'{subject_name}_{teacher_name}_{course_start_}']

            # 建立資料夾
            folderName1 = subject_name.replace(' ', '\ ')
            folderName2 = teacher_name.replace(' ', '\ ')
            course_start = course_start_.replace(' ', '\ ')
            google_drive.execute_shell_command(f"mkdir /Meet\ Recordings/原始檔案/{folderName1}/{folderName2}", print_file=False)
            google_drive.execute_shell_command(f"mkdir /Meet\ Recordings/暫存檔案/{folderName1}/{folderName2}", print_file=False)

            for i_ in range(len(classroom_Info[code_])):
                file_n = 0
                file_name_source = classroom_Info[code_][i_]['錄製檔案'].replace(' ', '\ ')
                # 複製檔案
                while True:
                    if file_n == 0:
                        file_name_target = f"{folderName1}_{folderName2}_{course_start}"
                    else:
                        file_name_target = f"{folderName1}_{folderName2}_{course_start}_({file_n})"
                    response = google_drive.execute_shell_command(f"cp /Meet\ Recordings/{file_name_source} /Meet\ Recordings/暫存檔案/{folderName1}/{folderName2}/{file_name_target}", print_file=False)
                    if response == '檔案已存在': file_n += 1
                    else: break

                # 搬移檔案
                file_n = 0
                while True:
                    if file_n == 0:
                        file_name_target = f"{folderName1}_{folderName2}_{course_start}"
                    else:
                        file_name_target = f"{folderName1}_{folderName2}_{course_start}_({file_n})"
                    response = google_drive.execute_shell_command(f"mv /Meet\ Recordings/{file_name_source} /Meet\ Recordings/原始檔案/{folderName1}/{folderName2}/{file_name_target}", print_file=False)
                    if response == '檔案已存在': file_n += 1
                    else: break

        for key_ in notify_info.keys():
            notify_info[key_] = set(notify_info[key_])
        return notify_info

    def line_notify_message(self, notifyInfo):
        message =f'\n 韓老師，本日影片已經備份，請至Google Drive查看\n'
        for key_ in notifyInfo.keys():
            message += f'{key_}:\n'
            for file_ in notifyInfo[key_]:
                message += f'{file_}\n'
        return message

if __name__ == '__main__':
    pass