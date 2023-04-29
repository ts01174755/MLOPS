import os
import env_config
import sys
from src.model.docker_cmd import DockerCmd
import time

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

if __name__ == "__main__":
    RUN = ['images', 'build', 'update', 'gpt_base', 'python_package', 'OTHER'][1]
    if RUN == 'images':
        # dockerCmd pull Images
        DockerCmd.dockerPull(tag=env_config.IMAGE_MONGODB_TAG)
        DockerCmd.dockerPull(tag=env_config.IMAGE_MONGODB_EXPRESS_TAG)

    elif RUN == 'build':
        # dockerCmd 建立網路
        DockerCmd.dockerNetworkCreate(name=f'bridge {env_config.CONTAINER_MONGO_POSTGRES_NET}')

        # dockerCmd run mongodb
        DockerCmd.dockerRun(
            tag=env_config.IMAGE_MONGODB_TAG,
            name=env_config.CONTAINER_MONGODB_NAME,
            port=env_config.CONTAINER_MONGODB_PORT_LIST,
            volume=f'{env_config.CONTAINER_MONGODB_ROOT_MAP}:{env_config.CONTAINER_MONGODB_ROOT}',
            envDict=env_config.CONTAINER_MONGO_ENV_DICT,
            # network='mongo-net',
            detach=True, interactive=False, TTY=False
        )

        # dockerCmd run dpage/pgadmin4:6.20
        DockerCmd.dockerRun(
            tag=env_config.IMAGE_MONGODB_EXPRESS_TAG,
            name=env_config.CONTAINER_MONGODB_EXPRESS_NAME,
            port=env_config.CONTAINER_MONGODB_EXPRESS_PORT_LIST,
            volume=f'{env_config.CONTAINER_MONGODB_EXPRESS_ROOT_MAP}:{env_config.CONTAINER_MONGODB_EXPRESS_ROOT}',
            envDict=env_config.CONTAINER_MONGO_EXPRESS_ENV_DICT,
            # network='mongo-net',
            detach=True, interactive=False, TTY=False
        )

        DockerCmd.dockerNetworkConnect(name=env_config.CONTAINER_MONGO_POSTGRES_NET, container=env_config.CONTAINER_MONGODB_NAME)
        DockerCmd.dockerNetworkConnect(name=env_config.CONTAINER_MONGO_POSTGRES_NET, container=env_config.CONTAINER_MONGODB_EXPRESS_NAME)

        time.sleep(5)
        os.system(f'open http://localhost:{env_config.CONTAINER_MONGODB_EXPRESS_PORT_LIST[0].split(":")[0]}')

    elif RUN == '手動':
        pass
        # MongoDB - 建立資料庫
        # >> 用mongo_express建Database
        # >> 或用mongodb Shell建Database
        # $ mongo -u mongodb -p mongodb --authenticationDatabase admin
        # > use originaldb

    elif RUN == 'update':
        # 更新apt-get
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_MONGO_POSTGRES_NET,
            cmd="apt-get update",
            detach=False,
            interactive=True,
            TTY=False,
        )
        # 更新pip
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_MONGO_POSTGRES_NET,
            cmd='bash -c "pip install --upgrade pip"',
            detach=False,
            interactive=True,
            TTY=False,
        )

    elif RUN == 'gpt_base':
        # dockerCmd postgres:15.2 - 基礎安裝
        apt_install_package = [
            'git', 'make', 'vim', 'libpq-dev', 'gcc', 'python', 'python3', 'python3-pip', 'unzip'
        ]
        for package in apt_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_MONGO_POSTGRES_NET,
                cmd=f'apt-get install -y {package}',
                detach=False,
                interactive=True,
                TTY=False,
            )
    elif RUN == 'python_package':
        # 更新pip
        python_install_package = [
            'psycopg2', 'psycopg2-binary', 'pymongo', 'requests', 'python-dotenv', 'beautifulsoup4',
            'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'google-auth', 'oauth2client'
        ]
        for package in python_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_MONGO_POSTGRES_NET,
                cmd=f'bash -c "pip install {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )
    elif RUN == 'OTHER':
        pass