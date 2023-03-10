import os;
import sys;
if len(sys.argv) > 1:
    print(sys.argv[1])
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from package.common.DatabaseCtrl import PostgresCtrl, MongoDBCtrl
from package.common.BS4Crawler import bs4Crawler
from dotenv import load_dotenv, find_dotenv
from DE_PostgresDB.package.PostgresParseSTData import PostgresParseSTData
from datetime import datetime
import time
import re

if __name__ == '__main__':
    # 連接儲存爬蟲DataBase
    load_dotenv(find_dotenv('env/.env'))
    postgresParseSTData = MLFlow(PostgresParseSTData())

    stData = postgresParseSTData.parseSTData()
    print(stData)