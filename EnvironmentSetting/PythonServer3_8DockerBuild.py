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

    # 建構Python3.8的Docker Image
    # dockerCmd pull Images
    dockerCmd.dockerPull(tag='python:3.8.16')
    dockerCmd.dockerRun(
        tag='python:3.8.16',
        name='python3.8.16',
        volume='/Users/peiyuwu/Development/docker/python3.8.16:/Users/peiyuwu',
        detach=True, interactive=True, TTY=False
    )

    ####################################################################################################################
    # dockerCmd postgres:15.2 - 基礎安裝
    dockerCmd.dockerExec(name='python3.8.16', cmd='apt-get update', detach=False, interactive=True, TTY=False)  # 更新 apt-get
    dockerCmd.dockerExec(name='python3.8.16', cmd='apt-get install -y git', detach=False, interactive=True, TTY=False)  # 安裝 git
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "apt-get install make"', detach=False, interactive=True, TTY=False)  # 安裝 make
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "apt-get install gcc -y"', detach=False, interactive=True, TTY=False)  # 安裝 gcc
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "apt-get install -y vim"', detach=False, interactive=True, TTY=False) # 安裝pip
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "apt-get install -y wget"', detach=False, interactive=True, TTY=False)  # 安裝 wget
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "apt-get install -y zlib1g-dev"', detach=False, interactive=True, TTY=False)  # 安裝 zlib1g-dev

    # python 常用安裝包
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "pip install --upgrade pip"', detach=False, interactive=True, TTY=False)  # 更新pip
    dockerCmd.dockerExec(name='python3.8.16', cmd='bash -c "pip3 install python-dotenv"', detach=False, interactive=True, TTY=False)  # 安裝 python-dotenv

