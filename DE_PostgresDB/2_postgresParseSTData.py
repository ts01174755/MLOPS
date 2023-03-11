import os;
import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from DE_PostgresDB.package.PostgresParseSTData import PostgresParseSTData
from datetime import datetime, timedelta
import time

if __name__ == '__main__':
    TODAY = time.localtime(time.time() + 8 * 60 * 60) # 時間校準
    TOMORROW = time.localtime(time.time() + 8 * 60 * 60 + 24 * 60 * 60) # 時間校準
    TABLE = sys.argv[2]

    # 每日執行 - 爬蟲
    postgresParseSTData = MLFlow(PostgresParseSTData())
    stData = postgresParseSTData.parseSTData(
        dt1 = time.strftime("%Y-%m-%d", TODAY),
        dt2 = time.strftime("%Y-%m-%d", TOMORROW)
    )

    # 連接PostgresDB與寫入資料
    postgresParseSTData.insertSTData(table = TABLE, dataList=stData, now=time.strftime("%Y-%m-%d %H:%M:%S", TODAY))

    # # 指定執行日期範圍
    # today = datetime(2023, 3, 9, 0, 0, 0)
    # while today < datetime(2023, 3, 11, 0, 0, 0):
    #     # 爬蟲
    #     stData = postgresParseSTData.parseSTData(
    #         dt1 = today.strftime('%Y-%m-%d'),
    #         dt2 = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #     )
    #     # print(stData)
    #
    #     # 連接PostgresDB與寫入資料
    #     postgresParseSTData.insertSTData(DataList=stData, now=today.strftime('%Y-%m-%d %H:%M:%S'))
    #
    #     # 往後一天
    #     today = today + timedelta(days=1)