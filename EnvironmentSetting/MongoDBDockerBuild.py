import os; os.chdir(os.path.dirname(os.path.abspath(__file__)).split('PostgresDB')[0])
import sys; sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
import time

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

if __name__ == '__main__':
    # 用工廠模式派生多個機器學習流程
    dockerCmd = MLFlow(DockerCmd())

    # # dockerCmd pull Images
    # # dockerCmd.dockerPull(tag='mongo:5.0.15')
    # # dockerCmd.dockerPull(tag='mongo-express:0.54.0')
    #
    # # dockerCmd 建立網路
    # dockerCmd.dockerNetworkRemove(name='mongo-net')
    # dockerCmd.dockerNetworkCreate(name='bridge mongo-net')
    #
    # # dockerCmd run mongodb
    # dockerCmd.dockerRun(
    #     tag='mongo:5.0.15',
    #     name='mongodb',
    #     port='27017:27017',
    #     volume='/Users/peiyuwu/Development/docker/mongodb:/Users/peiyuwu',
    #     envDict={'MONGO_INITDB_ROOT_USERNAME': 'mongodb', 'MONGO_INITDB_ROOT_PASSWORD': 'mongodb'},
    #     network='mongo-net',
    #     detach=True, interactive=False, TTY=False
    # )
    #
    # # dockerCmd run dpage/pgadmin4:6.20
    # dockerCmd.dockerRun(
    #     tag='mongo-express:0.54.0',
    #     name='mongo_express',
    #     port='8081:8081',
    #     volume='/Users/peiyuwu/Development/docker/mongo_express:/Users/peiyuwu',
    #     envDict={
    #         'ME_CONFIG_MONGODB_SERVER': 'mongodb',
    #         'ME_CONFIG_MONGODB_ADMINUSERNAME': 'mongodb',
    #         'ME_CONFIG_MONGODB_ADMINPASSWORD': 'mongodb',
    #         'ME_CONFIG_BASICAUTH_USERNAME': 'mongoUser',
    #         'ME_CONFIG_BASICAUTH_PASSWORD': 'mongoUserPassword'
    #     },
    #     network='mongo-net',
    #     detach=True, interactive=False, TTY=False
    # )
    # time.sleep(3)
    # os.system('open http://localhost:8081/')
    # ####################################################################################################################
    # # MongoDB - 建立資料庫
    # # >> 用mongo_express建Database
    # # >> 或用mongodb Shell建Database
    # # $ mongo -u mongodb -p mongodb --authenticationDatabase admin
    # # > use originaldb
    #
    # # ####################################################################################################################
    # # dockerCmd mongodb - 基礎安裝
    # dockerCmd.dockerExec(name='mongodb', cmd='apt-get update', detach=False, interactive=True, TTY=False)  # 更新 apt-get
    # dockerCmd.dockerExec(name='mongodb', cmd='apt-get install -y git', detach=False, interactive=True, TTY=False)  # 安裝 git
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install make"', detach=False, interactive=True, TTY=False)  # 安裝 make
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y vim"', detach=False, interactive=True, TTY=False) # 安裝pip
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y libpq-dev"', detach=False, interactive=True, TTY=False)  # 安裝 libpq-dev
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install gcc -y"', detach=False, interactive=True, TTY=False)  # 安裝 gcc
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y python"', detach=False, interactive=True, TTY=False) # 安裝python
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y python3"', detach=False, interactive=True, TTY=False) # 安裝python
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y python3-pip"', detach=False, interactive=True, TTY=False)  # 安裝 pip3
    #
    # ####################################################################################################################
    # # # python 常用安裝包
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install python-dotenv"', detach=False, interactive=True, TTY=False)  # 安裝 python-dotenv
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install psycopg2"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install psycopg2-binary"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2-binary
    # dockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install pymongo"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
    dockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install requests"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
    dockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install beautifulsoup4"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo