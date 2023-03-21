import os; import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.MongoDBCtrl import MongoDBCtrl
from DE_MongoDB.package.FuturesExchange import FuturesExchange
from dotenv import load_dotenv, find_dotenv
import time
import json

if __name__ == '__main__':
    load_dotenv(find_dotenv('env/.env'))
    load_dotenv(find_dotenv('env/.config'))
    TODAY = time.strftime("%Y_%m_%d", time.localtime(time.time() + 8 * 60 * 60 - 24 * 60 * 60))

    with open('env/futuresExchange.json', 'r') as f: futuresExchangeDict = json.load(f)
    FILENAME = f'Daily_{TODAY}.zip'
    URL = futuresExchangeDict['Futures_Dailydownload'].replace('[:FILENAME]', FILENAME)
    MONGODB_DOWNLOADS_PATH = os.getenv('MONGODB_DOWNLOADS_PATH') + '/' + FILENAME.split('.')[0]

    # 每日解析爬蟲資料
    futuresExchange = MLFlow(FuturesExchange())
    # 爬取每ㄖ期貨交易資料
    requestResponse = futuresExchange.get_futuresExchange_dailyFile(
        URL=URL,
        FILEPATH=MONGODB_DOWNLOADS_PATH
    )