import os
import env_config
from src.model.docker_cmd import DockerCmd

if __name__ == "__main__":
    # ------------------------ env_params ------------------------
    CONTAINER_NAME = env_config.CONTAINERNAME_PYTHON_3_8_18

    # 重啟docker container
    DockerCmd.dockerRestart(CONTAINER_NAME)

