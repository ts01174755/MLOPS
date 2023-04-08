import os

os.chdir(os.path.dirname(os.path.abspath(__file__)).split("PostgresDB")[0])
import sys

sys.path.append(os.getcwd())
from src.my_model.docker_cmd import DockerCmd

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

if __name__ == "__main__":
    # 建構Python3.8的Docker Image
    # dockerCmd pull Images
    # DockerCmd.dockerPull(tag='python:3.8.16')

    # DockerCmd.dockerRun(
    #     tag='python:3.8.16',
    #     name='python3.8.16',
    #     port=[f'{port}:{port}' for port in range(8000, 8010)],
    #     volume='/Users/peiyuwu/Development/docker/python3.8.16:/Users/peiyuwu',
    #     detach=True, interactive=True, TTY=False
    # )
    # DockerCmd.dockerNetworkConnect(name='mongo-postgres-net', container='python3.8.16')

    ####################################################################################################################
    # dockerCmd postgres:15.2 - 基礎安裝
    DockerCmd.dockerExec(
        name="python3.8.16",
        cmd="apt-get update",
        detach=False,
        interactive=True,
        TTY=False,
    )  # 更新 apt-get
    apt_install_package = ['tzdata', 'git', 'make', 'gcc', 'vim', 'wget', 'zlib1g-dev', '']
    for package in apt_install_package:
        DockerCmd.dockerExec(
            name='python3.8.16',
            cmd=f'apt-get install -y {package}',
            detach=False,
            interactive=True,
            TTY=False,
        )

    # python 常用安裝包
    DockerCmd.dockerExec(
        name="python3.8.16",
        cmd='bash -c "pip install --upgrade pip"',
        detach=False,
        interactive=True,
        TTY=False,
    )  # 更新pip
    python_install_package = [
        'python-dotenv', 'fastapi', 'uvicorn', 'psycopg2', 'pymongo', 'setuptools', 'requests', 'beautifulsoup4',
        'pandas', 'black', 'build', 'tree', 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib',
        'oauth2client', 'aiofiles', 'Jinja2==3.1.2', 'sqlalchemy'
    ]
    for package in python_install_package:
        DockerCmd.dockerExec(
            name='python3.8.16',
            cmd=f'bash -c "pip install {package}"',
            detach=False,
            interactive=True,
            TTY=False,
        )

    # docker 修改時區
    DockerCmd.dockerExec(
        name="python3.8.16",
        cmd='bash -c "ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime"',
        detach=False,
        interactive=True,
        TTY=False,
    )  # 修改時區
