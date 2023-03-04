import os; import sys;
if len(sys.argv) > 1:
    print(sys.argv[1])
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from package.common.DatabaseCtrl import Database
from dotenv import load_dotenv, find_dotenv



if __name__ == '__main__':

    load_dotenv(find_dotenv('env/.env'))

    # 連接儲存爬蟲DataBase
    db = MLFlow(Database(
        host=os.getenv('POSTGRES_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database='originaldb'
    ))
    db.connect()

    # 建立儲存爬蟲Schema
    db.execute('CREATE SCHEMA IF NOT EXISTS crawler;') # 建立Schema

    # 建立儲存爬蟲資料表
    db.execute('''
        CREATE TABLE IF NOT EXISTS crawler.original (\
        id serial PRIMARY KEY, dt timestamp, memo varchar(50)\
        , commondata varchar(50), commondata2 varchar(50), commondata3 varchar(50), commondata4 varchar(50), commondata5 varchar(50)\
        , commondata6 varchar(50), commondata7 varchar(50), commondata8 varchar(50), commondata9 varchar(50), commondata10 varchar(50)\
        , uniqueint int, uniqueint2 int, uniqueint3 int, uniqueint4 int, uniqueint5 int\
        , uniqueint6 int, uniqueint7 int, uniqueint8 int, uniqueint9 int, uniqueint10 int\
        , uniquefloat float, uniquefloat2 float, uniquefloat3 float, uniquefloat4 float, uniquefloat5 float\
        , uniquefloat6 float, uniquefloat7 float, uniquefloat8 float, uniquefloat9 float, uniquefloat10 float\
        , uniquefloat11 float, uniquefloat12 float, uniquefloat13 float, uniquefloat14 float, uniquefloat15 float\
        , uniquestring text, uniquestring2 text, uniquestring3 text, uniquestring4 text, uniquestring5 text\
        , uniquejason json\
        );
    ''') # 建立資料表

    # 插入測試資料
    db.execute("INSERT INTO crawler.original (dt, memo, commondata, uniqueint, uniquefloat, uniquestring, uniquejason) VALUES (now(), 'test', 'test', 1, 1.1, 'test', '{\"test\":1}');")  # 插入資料
    # 刪除測試資料
    db.execute('DELETE FROM crawler.original WHERE memo = \'test\';') # 刪除資料
    db.close()
