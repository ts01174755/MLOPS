import os; import sys;
if len(sys.argv) > 1: os.chdir(os.path.dirname(os.path.abspath(__file__)).split(sys.argv[1])[0])
sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from dotenv import load_dotenv, find_dotenv



if __name__ == '__main__':

    load_dotenv(find_dotenv('env/.env'))
    if os.getenv('ROLE') != 'postgres15.2':
        print('containerName is not postgres15.2')

        PROJECTNAME = 'PostgresDB'
        mlflow = MLFlow()
        # 用dockerDeploy()把gitHub上的程式碼clone到docker container中
        mlflow.deploy(
            containerName='postgres15.2',
            gitHubUrl='https://github.com/ts01174755/MLOPS.git',
            targetPath='/Users/peiyuwu/MLOPS',
            envPATH='/Users/peiyuwu/MLOPS/PostgresDB/.env'
        )

        # 用dockerCI()把現在執行的程式更新到container中
        mlflow.CI(
            containerName='postgres15.2',
            filePath='/PostgresDB/1_postgresCreateDB.py',
            targetPath='/Users/peiyuwu/MLOPS/PostgresDB/2_postgresCreateTable.py',
        )

        # 用dockerCD()在container中執行程式
        mlflow.CD(
            containerName='postgres15.2',
            interpreter='python3.9',
            targetPath='/Users/peiyuwu/MLOPS/PostgresDB/2_postgresCreateTable.py',
            paramArgs=f'{PROJECTNAME}'
        )
    else:
        print('containerName is postgres15.2')
        # 這裡是程式主體
        ...


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