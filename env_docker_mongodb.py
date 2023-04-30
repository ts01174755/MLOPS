import os
import env_config
import sys
from src.model.docker_cmd import DockerCmd
import time
import subprocess

## params
# RUN = ['images', 'build', 'pkg_init', 'gpt_base', 'python_package', 'OTHER', 'all']
RUN = 'images' if len(sys.argv) == 1 else sys.argv[1]

if __name__ == "__main__":
    if RUN == 'images' or RUN == 'all':
        # dockerCmd pull Images
        DockerCmd.dockerPull(tag=env_config.IMAGE_MONGODB_TAG)
        DockerCmd.dockerPull(tag=env_config.IMAGE_MONGODB_EXPRESS_TAG)

    if RUN == 'build' or RUN == 'all':
        # dockerCmd 建立網路
        DockerCmd.dockerNetworkRemove(name=f'{env_config.CONTAINER_MONGO_POSTGRES_NET}')
        DockerCmd.dockerNetworkCreate(name=f'{env_config.CONTAINER_MONGO_POSTGRES_NET}')

        subprocess.run(f"mkdir -p {env_config.CONTAINER_MONGODB_ROOT_MAP}", shell=True)
        subprocess.run(f"mkdir -p {env_config.CONTAINER_MONGODB_EXPRESS_ROOT_MAP}", shell=True)

        # dockerCmd run mongodb
        DockerCmd.dockerRun(
            tag=env_config.IMAGE_MONGODB_TAG,
            name=env_config.CONTAINER_MONGODB_NAME,
            port=env_config.CONTAINER_MONGODB_PORT_LIST,
            volume=f'{env_config.CONTAINER_MONGODB_ROOT_MAP}:{env_config.CONTAINER_MONGODB_ROOT}',
            envDict=env_config.CONTAINER_MONGO_ENV_DICT,
            network=env_config.CONTAINER_MONGO_POSTGRES_NET,
            detach=True, interactive=False, TTY=False
        )

        # dockerCmd run dpage/pgadmin4:6.20
        DockerCmd.dockerRun(
            tag=env_config.IMAGE_MONGODB_EXPRESS_TAG,
            name=env_config.CONTAINER_MONGODB_EXPRESS_NAME,
            port=env_config.CONTAINER_MONGODB_EXPRESS_PORT_LIST,
            volume=f'{env_config.CONTAINER_MONGODB_EXPRESS_ROOT_MAP}:{env_config.CONTAINER_MONGODB_EXPRESS_ROOT}',
            envDict=env_config.CONTAINER_MONGO_EXPRESS_ENV_DICT,
            network=env_config.CONTAINER_MONGO_POSTGRES_NET,
            detach=True, interactive=False, TTY=False
        )

        time.sleep(5)
        os.system(f'open http://localhost:{env_config.CONTAINER_MONGODB_EXPRESS_PORT_LIST[0].split(":")[0]}')

    if RUN == 'pkg_init' or RUN == 'all':
        # 更新apt-get
        DockerCmd.dockerExec(
            name=env_config.CONTAINER_MONGODB_NAME,
            cmd="apt-get update",
            detach=False,
            interactive=True,
            TTY=False,
        )

    if RUN == 'gpt_base' or RUN == 'all':
        apt_install_package = [
            'git', 'make', 'vim', 'libpq-dev', 'gcc', 'python', 'python3', 'python3-pip', 'unzip'
        ]
        for package in apt_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_MONGODB_NAME,
                cmd=f'bash -c "apt-get install -y {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )

    if RUN == 'python_package' or RUN == 'all':
        # 更新pip
        python_install_package = [
            'psycopg2', 'psycopg2-binary', 'pymongo', 'requests', 'python-dotenv', 'beautifulsoup4',
            'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'google-auth', 'oauth2client'
        ]
        for package in python_install_package:
            DockerCmd.dockerExec(
                name=env_config.CONTAINER_MONGODB_NAME,
                cmd=f'bash -c "pip install {package}"',
                detach=False,
                interactive=True,
                TTY=False,
            )
    if RUN == 'OTHER':
        pass