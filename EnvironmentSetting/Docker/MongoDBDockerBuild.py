import os; 
import sys; sys.path.append(os.getcwd())
from package.Environment.DockerCmd import DockerCmd
import time
from config import MongoDB, MongoExpress

BUILD_ENV = sys.argv[1]
STEP = sys.argv[2]


if __name__ == '__main__':    
    # Step 1: dockerCmd pull Image
    if BUILD_ENV == 'MongoDB':
        MongoDB = MongoDB()

        if STEP == 'pull_image':
            DockerCmd.dockerPull(tag = MongoDB.tag)
            DockerCmd.dockerNetworkRemove(name='mongo-net')
            DockerCmd.dockerNetworkCreate(name='bridge mongo-net')

        # Step 2: dockerCmd run mongodb
        if STEP == 'docker_run':
            # 檢查docker映射目錄是否存在
            if not os.path.exists(MongoDB.volume.split(':')[0]):
                os.makedirs(MongoDB.volume.split(':')[0])

            DockerCmd.dockerRun(tag = MongoDB.tag,
                                name = MongoDB.name,
                                port = MongoDB.port,
                                volume = MongoDB.volume,
                                envDict = MongoDB.envDict,
                                network = MongoDB.network,
                                detach=True, interactive=False, TTY=False
                                )
    

    if BUILD_ENV == 'MongoExpress':
        MongoExpress = MongoExpress()

        if STEP == 'pull_image':
            # dockerCmd 建立網路
            DockerCmd.dockerPull(tag = MongoExpress.tag)
        # Step 2: dockerCmd run mongodb
        if STEP == 'docker_run':
            # 檢查docker映射目錄是否存在
            if not os.path.exists(MongoExpress.volume.split(':')[0]):
                os.makedirs(MongoExpress.volume.split(':')[0])

            # dockerCmd run dpage/pgadmin4:6.20
            DockerCmd.dockerRun(tag = MongoExpress.tag,
                                name = MongoExpress.name,
                                port = MongoExpress.port,
                                volume = MongoExpress.volume,
                                envDict = MongoExpress.envDict,
                                network = MongoExpress.network,
                                detach=True, interactive=False, TTY=False
                                )
    
            time.sleep(3)
            os.system('open http://localhost:8081/')
    # ####################################################################################################################
    # # MongoDB - 建立資料庫
    # # >> 用mongo_express建Database
    # # >> 或用mongodb Shell建Database
    # # $ docker exec -it mongodb bash
    # # $ mongo -u mongodb -p mongodb --authenticationDatabase admin
    # # > use originaldb # 建立mongodb 的db
    #
    # # ####################################################################################################################
    if BUILD_ENV == 'Mongo_PythonEnv':
        # Step 3: dockerCmd mongodb - 基礎安裝
        DockerCmd.dockerExec(name='mongodb', cmd='apt-get update', detach=False, interactive=True, TTY=False)  # 更新 apt-get
        DockerCmd.dockerExec(name='mongodb', cmd='apt-get install -y git', detach=False, interactive=True, TTY=False)  # 安裝 git
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install make"', detach=False, interactive=True, TTY=False)  # 安裝 make
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y vim"', detach=False, interactive=True, TTY=False) # 安裝pip
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y libpq-dev"', detach=False, interactive=True, TTY=False)  # 安裝 libpq-dev
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install gcc -y"', detach=False, interactive=True, TTY=False)  # 安裝 gcc
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y python"', detach=False, interactive=True, TTY=False) # 安裝python
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y python3"', detach=False, interactive=True, TTY=False) # 安裝python
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "apt-get install -y python3-pip"', detach=False, interactive=True, TTY=False)  # 安裝 pip3
        #
        # ####################################################################################################################
        # # python 常用安裝包
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install python-dotenv"', detach=False, interactive=True, TTY=False)  # 安裝 python-dotenv
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install psycopg2"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install psycopg2-binary"', detach=False, interactive=True, TTY=False)  # 安裝 psycopg2-binary
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install pymongo"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install requests"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install beautifulsoup4"', detach=False, interactive=True, TTY=False)  # 安裝 pymongo

        # # 安裝 google form 相關的套件
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install google-api-python-client"', detach=False, interactive=True, TTY=False)  # 安裝 google-api-python-client
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install google-auth-httplib2"', detach=False, interactive=True, TTY=False)  # 安裝 google-auth-httplib2
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install google-auth-oauthlib"', detach=False, interactive=True, TTY=False)  # 安裝 google-auth-oauthlib
        DockerCmd.dockerExec(name='mongodb', cmd='bash -c "pip3 install oauth2client"', detach=False, interactive=True, TTY=False)  # 安裝 google-auth

