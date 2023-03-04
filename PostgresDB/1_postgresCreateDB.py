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

    db = MLFlow(Database(
        host=os.getenv('POSTGRES_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database='testdb'
    ))

    db.connect()


    # # dockerCmd postgres:15.2 - 建立資料庫
    # dockerCmd.dockerExec(
    #     name='postgres15.2',
    #     cmd="psql -U postgres -c \'CREATE DATABASE testdb;\'",
    #     detach=False, interactive=True, TTY=False
    # )  # 建立資料庫 testdb
    #
    # # dockerCmd postgres:15.2 - 建立Schema
    # dockerCmd.dockerExec(
    #     name='postgres15.2',
    #     cmd="psql -U postgres -d testdb -c \'CREATE SCHEMA testschema;\'",
    #     detach=False, interactive=True, TTY=False
    # )  # 建立Schema testschema
    #
    # # dockerCmd postgres:15.2 - 建立資料表
    # dockerCmd.dockerExec(
    #     name='postgres15.2',
    #     cmd="psql -U postgres -d testdb -c \'CREATE TABLE testtable (id serial PRIMARY KEY, name varchar(50), value int);\'",
    #     detach=False, interactive=True, TTY=False
    # )  # 建立資料表 testtable
    #
    # # dockerCmd postgres:15.2 - 刪除資料表
    # dockerCmd.dockerExec(name='postgres15.2', cmd="psql -U postgres -d testdb -c \'DROP TABLE testtable;\'", detach=False, interactive=True, TTY=False)  # 刪除資料表 testtable
    #
    # # dockerCmd postgres:15.2 - 建立分區表
    # dockerCmd.dockerExec(
    #     name='postgres15.2',
    #     cmd='bash -c "psql -U postgres -d testdb -c \'CREATE TABLE testtable (id serial, name varchar(50), value int, PRIMARY KEY (id, value)) PARTITION BY RANGE (value);\'"',
    #     detach=False, interactive=True, TTY=False
    # )  # 建立資料表 testtable
    #

    # 測試資料庫連線
    db.connect()
    db.execute('CREATE TABLE IF NOT EXISTS testschema.test (num integer, data varchar);') # 建立資料表
    db.execute("INSERT INTO testschema.test (num, data) VALUES (100, 'abc');")  # 插入資料
    rows = db.query('SELECT * FROM testschema.test;')
    db.execute('DROP TABLE IF EXISTS testschema.test;') # 如果存在就刪除
    db.close()
    print(rows)