import os
import env_config
import sys
from src.model.docker_cmd import DockerCmd

# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

if __name__ == "__main__":
    RUN = ['images', 'build', 'update', 'gpt_base', 'python_package', 'OTHER'][1]
    if RUN == 'images':
        # 建構Python3.8的Docker Image
        # dockerCmd pull Images
        DockerCmd.dockerPull(tag=env_config.IMAGE_PYTHON_3_8_18_TAG)

    elif RUN == 'build':
        DockerCmd.dockerRun(
            tag=env_config.IMAGE_PYTHON_3_8_18_TAG,
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            port=env_config.CONTAINER_PYTHON_3_8_18_PORT_LIST,
            volume=f'{env_config.CONTAINER_PYTHON_3_8_18_ROOT_MAP}:{env_config.CONTAINER_PYTHON_3_8_18_ROOT}',
            detach=True, interactive=True, TTY=False
        )
        DockerCmd.dockerNetworkConnect(name=env_config.CONTAINER_MONGO_POSTGRES_NET, container=env_config.CONTAINER_PYTHON_3_8_18_NAME)

        # 建立基礎Folder
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd=f'bash -c "mkdir -p {env_config.CONTAINER_PYTHON_3_8_18_FILE_PATH}"',
            detach=False,
            interactive=True,
            TTY=False
        )
        # 建立基礎Folder
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd=f'bash -c "mkdir -p {env_config.CONTAINER_PYTHON_3_8_18_DOWNLOAD_PATH}"',
            detach=False,
            interactive=True,
            TTY=False
        )

    elif RUN == 'update':
        # 更新apt-get
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd="apt-get update",
            detach=False,
            interactive=True,
            TTY=False,
        )
        # 更新pip
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd='bash -c "pip install --upgrade pip"',
            detach=False,
            interactive=True,
            TTY=False,
        )

    elif RUN == 'gpt_base':
        # dockerCmd postgres:15.2 - 基礎安裝
        apt_install_package = ['tzdata', 'git', 'make', 'gcc', 'vim', 'wget', 'zlib1g-dev', '']
        for package in apt_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
                cmd=f'apt-get install -y {package}',
                detach=False,
                interactive=True,
                TTY=False,
            )

    elif RUN == 'python_package':
        # 更新pip
        python_install_package = [
            'python-dotenv', 'fastapi', 'uvicorn', 'psycopg2', 'pymongo', 'setuptools', 'requests', 'beautifulsoup4',
            'pandas', 'black', 'build', 'tree', 'google-api-python-client', 'google-auth', 'google-auth-oauthlib',
            'google-auth-httplib2', 'oauth2client', 'aiofiles', 'Jinja2==3.1.2', 'sqlalchemy'
        ]
        for package in python_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
                cmd=f'bash -c "pip install {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )

    elif RUN == 'OTHER':
        # docker 修改時區
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd='bash -c "ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime"',
            detach=False,
            interactive=True,
            TTY=False,
        )  # 修改時區

    elif RUN == 'TEMP':
        # 顯示已安裝的python套件
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
            cmd='bash -c "pip list"',
            detach=False,
            interactive=True,
            TTY=False,
        )

        # 卸載python pkg
        python_install_package = ['oauth2client']
        for package in python_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_PYTHON_3_8_18_NAME,
                cmd=f'bash -c "pip uninstall -y {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )