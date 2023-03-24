import os; import sys;
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.PostgresCtrl import PostgresCtrl
from dotenv import load_dotenv, find_dotenv



if __name__ == '__main__':

    # 連接儲存原始區DataBase
    load_dotenv(find_dotenv('env/.env'))
    db = MLFlow(PostgresCtrl(
        host=os.getenv('POSTGRES_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database='originaldb'
    ))
    db.connect()

    # TABLE = 'temptb' # 這是測試用的table
    # TABLE = 'st_all_data' # 這是正式用的table
    TABLE = 'google_form' # 這是正式用的table

    # 刪除儲存原始區Schema
    # db.execute('DROP SCHEMA IF EXISTS original CASCADE;')

    # 建立儲存原始區Schema
    # db.execute('CREATE SCHEMA IF NOT EXISTS original;') # 建立Schema

    # 刪除儲存原始區資料表
    db.execute(f'DROP TABLE IF EXISTS original.{TABLE};')

    # 建立儲存原始區資料表
    db.execute(f'''
        CREATE TABLE IF NOT EXISTS original.{TABLE} (\
        id serial PRIMARY KEY, dt timestamp, memo varchar(50)\
        , commondata1 varchar(50), commondata2 varchar(50), commondata3 varchar(50), commondata4 varchar(50), commondata5 varchar(50)\
        , commondata6 varchar(50), commondata7 varchar(50), commondata8 varchar(50), commondata9 varchar(50), commondata10 varchar(50)\
        , uniquechar1 varchar(50), uniquechar2 varchar(50), uniquechar3 varchar(50), uniquechar4 varchar(50), uniquechar5 varchar(50)\
        , uniquechar6 varchar(50), uniquechar7 varchar(50), uniquechar8 varchar(50), uniquechar9 varchar(50), uniquechar10 varchar(50)\
        , uniqueint1 int, uniqueint2 int, uniqueint3 int, uniqueint4 int, uniqueint5 int\
        , uniqueint6 int, uniqueint7 int, uniqueint8 int, uniqueint9 int, uniqueint10 int\
        , uniquefloat1 float, uniquefloat2 float, uniquefloat3 float, uniquefloat4 float, uniquefloat5 float\
        , uniquefloat6 float, uniquefloat7 float, uniquefloat8 float, uniquefloat9 float, uniquefloat10 float\
        , uniquefloat11 float, uniquefloat12 float, uniquefloat13 float, uniquefloat14 float, uniquefloat15 float\
        , uniquestring1 text, uniquestring2 text, uniquestring3 text, uniquestring4 text, uniquestring5 text\
        , uniquejason json\
        );
    ''') # 建立資料表

    # # 插入測試資料
    # db.execute("INSERT INTO original.st_all_data (dt, memo, commondata, uniqueint, uniquefloat, uniquestring, uniquejason) VALUES (now(), 'test', 'test', 1, 1.1, 'test', '{\"test\":1}');")  # 插入資料
    # # 撈取測試資料
    # rows = db.query('SELECT * FROM crawler.original WHERE memo = \'test\';') # 撈取資料
    # print(rows)
    #
    # # 刪除測試資料
    # db.execute('DELETE FROM crawler.original WHERE memo = \'test\';') # 刪除資料
    db.close()
