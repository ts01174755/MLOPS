import os;
import sys; sys.path.append(os.getcwd())
import json
from package.Environment.DockerCmd import DockerCmd
import time
from config import PostgresSQL, PostgresSQLadmin

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

BUILD_ENV = sys.argv[1]
STEP = sys.argv[2]


if __name__ == '__main__':
    # Step 1: dockerCmd pull Image
    if BUILD_ENV == 'PostgresSQL':
        PostgresSQL = PostgresSQL()
        if STEP == 'pull_image':
            # dockerCmd pull Images
            DockerCmd.dockerPull(tag=PostgresSQL.tag)
        if STEP == 'docker_run':
            if not os.path.exists(PostgresSQL.volume.split(':')[0]):
                os.makedirs(PostgresSQL.volume.split(':')[0])
            # dockerCmd run postgres:15.2
            DockerCmd.dockerRun(
                tag=PostgresSQL.tag,
                name=PostgresSQL.name,
                port=PostgresSQL.port,
                volume=PostgresSQL.volume,
                envDict=PostgresSQL.envDict,
                detach=True, interactive=False, TTY=False)

    if BUILD_ENV == 'PostgresSQLadmin':
        PostgresSQLadmin = PostgresSQLadmin()
        if STEP == 'pull_image':
            DockerCmd.dockerPull(tag=PostgresSQLadmin.tag)
        if STEP == 'docker_run':
            # dockerCmd run dpage/pgadmin4:6.20
            DockerCmd.dockerRun(
                tag=PostgresSQLadmin.tag,
                name=PostgresSQLadmin.name,
                port=PostgresSQLadmin.port,
                volume=PostgresSQLadmin.volume,
                envDict=PostgresSQLadmin.envDict,
                detach=True, interactive=False, TTY=False)

            time.sleep(3)
            # 查看 postgres:15.2 的 container 的資訊
            cmdStr = DockerCmd.dockerInspect(name='postgres15.2') # 查看 container 資訊，找出Networks.bridge.IPAddress
            with open('./env/postgres_ipaddress.json', 'w') as f:
                json.dump(cmdStr, f)
            # 把cmdStr的資料寫進docker裡
            path_in_docker = PostgresSQLadmin.volume.split(':')[1]           
            DockerCmd.dockerWrite(name = 'postgres15.2', 
                                  path = path_in_docker + '/dockerInspect.txt', 
                                  data = cmdStr) # 查看 container 資訊，找出Networks.bridge.IPAddress
            os.system('open http://localhost:5050/') # 開啟 pgadmin4
            ####################################################################################################################
            ## 如何用pdadmin建立一台Server ## 
            # >> 點擊 "Add Server"
            # >> Name: postgresdb
            # >> Host name/address: {Networks.bridge.IPAddress}
            # >> Port: 5432
            # >> Maintenance database: postgres
            # >> Username: postgres
            # >> Password: postgres
            ####################################################################################################################


    if BUILD_ENV == 'PostgresSQL_PythonEnv':
        # # dockerCmd postgres:15.2 - 基礎安裝
        DockerCmd.dockerExec(name='postgres15.2', cmd='apt-get update', detach=False, interactive=True, TTY=False)  # 更新 apt-get
        DockerCmd.dockerExec(name='postgres15.2', cmd='apt-get install -y git', detach=False, interactive=True, TTY=False)  # 安裝 git
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install make"', detach=False, interactive=True, TTY=False)  # 安裝 make
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install gcc -y"', detach=False, interactive=True, TTY=False)  # 安裝 gcc
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y vim"', detach=False, interactive=True, TTY=False) # 安裝pip
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y wget"', detach=False, interactive=True, TTY=False)  # 安裝 wget
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y zlib1g-dev"', detach=False, interactive=True, TTY=False)  # 安裝 zlib1g-dev
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python"', detach=False, interactive=True, TTY=False) # 安裝python
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python3"', detach=False, interactive=True, TTY=False) # 安裝python
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python3-pip"', detach=False, interactive=True, TTY=False) # 安裝pip

        # python 常用安裝包
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install python-dotenv"', detach=False, interactive=True, TTY=False)  # 安裝 python-dotenv
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install psycopg2-binary"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2-binary
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install pymongo"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install requests"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install beautifulsoup4"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
        DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install pandas"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
        

    ####################################################################################################################
    # # 用 network 把 postgres15.2 和 mongodb 連起來
    # # dockerCmd 建立網路
    # DockerCmd.dockerNetworkRemove(name='mongo-postgres-net')
    # DockerCmd.dockerNetworkCreate(name='bridge mongo-postgres-net')

    # # 查看 docker 所有網路
    # DockerCmd.dockerNetworkLs()

    # # dockerCmd 把 postgres15.2 和 mongodb 加入網路
    # DockerCmd.dockerNetworkConnect(name='mongo-postgres-net', container='postgres15.2')
    # DockerCmd.dockerNetworkConnect(name='mongo-postgres-net', container='mongodb')
    # DockerCmd.dockerNetworkConnect(name='mongo-postgres-net', container='python:3.8.16')


    # ####################################################################################################################
    # # dockerCmd postgres:15.2 - 建立資料庫
    # DockerCmd.dockerExec(
    #     name='postgres15.2',
    #     cmd="psql -U postgres -c \'CREATE DATABASE originaldb;\'",
    #     detach=False, interactive=True, TTY=False
    # )  # 建立資料庫 crawlerdb




