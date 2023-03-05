import os; os.chdir(os.path.dirname(os.path.abspath(__file__)).split('PostgresDB')[0])
import sys; sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

if __name__ == '__main__':
    # 用工廠模式派生多個機器學習流程
    dockerCmd = MLFlow(DockerCmd())

    # dockerCmd pull Images
    # dockerCmd.dockerPull(tag='postgres:15.2')
    # dockerCmd.dockerPull(tag='dpage/pgadmin4:6.20')

    # dockerCmd run postgres:15.2
    dockerCmd.dockerRun(
        tag='postgres:15.2',
        name='postgres15.2',
        port='5432:5432',
        volume='/Users/peiyuwu/Development/docker/postgres15.2:/Users/peiyuwu',
        envDict={'POSTGRES_USER': 'postgres', 'POSTGRES_PASSWORD': 'postgres', 'POSTGRES_DB': 'postgres'},
        detach=True, interactive=False, TTY=False
    )

    # dockerCmd run dpage/pgadmin4:6.20
    dockerCmd.dockerRun(
        tag='dpage/pgadmin4:6.20',
        name='pgadmin4',
        port='5050:80',
        volume='/Users/peiyuwu/Development/docker/pgadmin4:/Users/peiyuwu',
        envDict={'PGADMIN_DEFAULT_EMAIL': 'pgadmin4@gmail.com', 'PGADMIN_DEFAULT_PASSWORD': 'pgadmin4'},
        detach=True, interactive=False, TTY=False
    )

    # 查看 postgres:15.2 的 container 的資訊
    cmdStr = dockerCmd.dockerInspect(name='postgres15.2') # 查看 container 資訊，找出Networks.bridge.IPAddress

    # 把cmdStr的資料寫進docker裡
    dockerCmd.dockerWrite(name='postgres15.2', path='/Users/peiyuwu/dockerInspect.txt', data=cmdStr) # 查看 container 資訊，找出Networks.bridge.IPAddress
    os.system('open http://localhost:5050/') # 開啟 pgadmin4
    # >> 點擊 "Add Server"
    # >> Name: postgresdb
    # >> Host name/address: {Networks.bridge.IPAddress}
    # >> Port: 5432
    # >> Maintenance database: postgres
    # >> Username: postgres
    # >> Password: postgres

    ####################################################################################################################
    # dockerCmd postgres:15.2 - 建立資料庫
    dockerCmd.dockerExec(
        name='postgres15.2',
        cmd="psql -U postgres -c \'CREATE DATABASE originaldb;\'",
        detach=False, interactive=True, TTY=False
    )  # 建立資料庫 crawlerdb


    ####################################################################################################################
    # # dockerCmd postgres:15.2 - 基礎安裝
    dockerCmd.dockerExec(name='postgres15.2', cmd='apt-get update', detach=False, interactive=True, TTY=False)  # 更新 apt-get
    dockerCmd.dockerExec(name='postgres15.2', cmd='apt-get install -y git', detach=False, interactive=True, TTY=False)  # 安裝 git
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install make"', detach=False, interactive=True, TTY=False)  # 安裝 make
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install gcc -y"', detach=False, interactive=True, TTY=False)  # 安裝 gcc
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y vim"', detach=False, interactive=True, TTY=False) # 安裝pip
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y wget"', detach=False, interactive=True, TTY=False)  # 安裝 wget
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y zlib1g-dev"', detach=False, interactive=True, TTY=False)  # 安裝 zlib1g-dev
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python"', detach=False, interactive=True, TTY=False) # 安裝python
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python3"', detach=False, interactive=True, TTY=False) # 安裝python
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install -y python3-pip"', detach=False, interactive=True, TTY=False) # 安裝pip

    # python 常用安裝包
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install python-dotenv"', detach=False, interactive=True, TTY=False)  # 安裝 python-dotenv
    dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "pip3 install psycopg2-binary"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2-binary




    ################################################## 不確定要不要用 #####################################################
    #
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install postgresql-contrib -y"', detach=False, interactive=True, TTY=False)  # 安裝 postgresql-contrib
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "apt-get install postgresql-server-dev-15 -y"', detach=False, interactive=True, TTY=False)  # 安裝 postgresql-server-dev-15
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "cd usr/share/postgresql/15/contrib && git clone https://github.com/pgpartman/pg_partman.git"', detach=False, interactive=True, TTY=False)  # 下載 pg_partman, https://github.com/pgpartman/pg_partman
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "cd usr/share/postgresql/15/contrib/pg_partman && make && make install"', detach=False, interactive=True, TTY=False)  # 安裝 pg_partman, https://dbastreet.com/?p=1447
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "cd usr/share/postgresql/15/contrib/pg_partman && make installcheck"', detach=False, interactive=True, TTY=False)  # 測試 pg_partman


    # # 安裝python3.8.16
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "wget https://www.python.org/ftp/python/3.8.16/Python-3.8.16.tgz"', detach=False, interactive=True, TTY=False)  # 下載 python3.8.16
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "tar -zxvf Python-3.8.16.tgz"', detach=False, interactive=True, TTY=False)  # 解壓縮 python3.8.16
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "cd Python-3.8.16 && ./configure --enable-optimizations"', detach=False, interactive=True, TTY=False)  # 安裝 python3.8.16
    # dockerCmd.dockerExec(name='postgres15.2', cmd='bash -c "cd Python-3.8.16 && make altinstall"', detach=False, interactive=True, TTY=False)  # 安裝 python3.8.16