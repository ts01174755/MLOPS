import os

os.chdir(os.path.dirname(os.path.abspath(__file__)).split("PostgresDB")[0])
import sys

sys.path.append(os.getcwd())
from src.my_model.docker_cmd import DockerCmd
import time

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

if __name__ == "__main__":
    # dockerCmd pull Images
    # DockerCmd.dockerPull(tag='postgres:15.2')
    # DockerCmd.dockerPull(tag='dpage/pgadmin4:6.20')

    # # dockerCmd run postgres:15.2
    # DockerCmd.dockerRun(
    #     tag='postgres:15.2',
    #     name='postgres15.2',
    #     port='5432:5432',
    #     volume='/Users/peiyuwu/Development/docker/postgres15.2:/Users/peiyuwu',
    #     envDict={'POSTGRES_USER': 'postgres', 'POSTGRES_PASSWORD': 'postgres', 'POSTGRES_DB': 'postgres'},
    #     detach=True, interactive=False, TTY=False
    # )
    #
    # # dockerCmd run dpage/pgadmin4:6.20
    # DockerCmd.dockerRun(
    #     tag='dpage/pgadmin4:6.20',
    #     name='pgadmin4',
    #     port='5050:80',
    #     volume='/Users/peiyuwu/Development/docker/pgadmin4:/Users/peiyuwu',
    #     envDict={'PGADMIN_DEFAULT_EMAIL': 'pgadmin4@gmail.com', 'PGADMIN_DEFAULT_PASSWORD': 'pgadmin4'},
    #     detach=True, interactive=False, TTY=False
    # )
    # time.sleep(3)
    #
    # # 查看 postgres:15.2 的 container 的資訊
    cmdStr = DockerCmd.dockerInspect(name='postgres15.2') # 查看 container 資訊，找出Networks.bridge.IPAddress
    #
    # # 把cmdStr的資料寫進docker裡
    DockerCmd.dockerWrite(name='postgres15.2', path='/Users/peiyuwu/dockerInspect.txt', data=cmdStr) # 查看 container 資訊，找出Networks.bridge.IPAddress
    # os.system('open http://localhost:5050/') # 開啟 pgadmin4
    # # >> 點擊 "Add Server"
    # # >> Name: postgresdb
    # # >> Host name/address: {Networks.bridge.IPAddress}
    # # >> Port: 5432
    # # >> Maintenance database: postgres
    # # >> Username: postgres
    # # >> Password: postgres

    ####################################################################################################################
    # 用 network 把 postgres15.2 和 mongodb 連起來
    # dockerCmd 建立網路

    # 查看 docker 所有網路
    # DockerCmd.dockerNetworkLs()

    # dockerCmd 把 postgres15.2 和 mongodb 加入網路
    # DockerCmd.dockerNetworkConnect(name="mongo-postgres-net", container="postgres15.2")

    #
    # ####################################################################################################################
    # # dockerCmd postgres:15.2 - 建立資料庫
    # DockerCmd.dockerExec(
    #     name='postgres15.2',
    #     cmd="psql -U postgres -c \'CREATE DATABASE originaldb;\'",
    #     detach=False, interactive=True, TTY=False
    # )  # 建立資料庫 crawlerdb
    #
    #
    # ####################################################################################################################
    # # # dockerCmd postgres:15.2 - 基礎安裝
    # DockerCmd.dockerExec(name='postgres15.2', cmd='apt-get update', detach=False, interactive=True, TTY=False)  # 更新 apt-get
    # DockerCmd.dockerExec(name='postgres15.2', cmd='apt-get install -y git', detach=False, interactive=True, TTY=False)  # 安裝 git
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install make"', detach=False, interactive=True, TTY=False)  # 安裝 make
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install gcc -y"', detach=False, interactive=True, TTY=False)  # 安裝 gcc
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y vim"', detach=False, interactive=True, TTY=False) # 安裝pip
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y wget"', detach=False, interactive=True, TTY=False)  # 安裝 wget
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y zlib1g-dev"', detach=False, interactive=True, TTY=False)  # 安裝 zlib1g-dev
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python"', detach=False, interactive=True, TTY=False) # 安裝python
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python3"', detach=False, interactive=True, TTY=False) # 安裝python
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python3-pip"', detach=False, interactive=True, TTY=False) # 安裝pip
    #
    # # python 常用安裝包
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install python-dotenv"', detach=False, interactive=True, TTY=False)  # 安裝 python-dotenv
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install psycopg2-binary"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2-binary
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install pymongo"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install requests"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install beautifulsoup4"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install pandas"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
    #
    # # 安裝 google form api 相關的套件
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install google-api-python-client"', detach=False, interactive=True, TTY=False)  # 安裝 google-api-python-client
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install google-auth-httplib2"', detach=False, interactive=True, TTY=False)  # 安裝 google-auth-httplib2
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install google-auth-oauthlib"', detach=False, interactive=True, TTY=False)  # 安裝 google-auth-oauthlib
    # DockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install oauth2client"', detach=False, interactive=True, TTY=False)  # 安裝 google-auth
    #
