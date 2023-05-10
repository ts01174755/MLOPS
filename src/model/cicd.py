import os
from src.model.docker_cmd import DockerCmd


class CICD:
    def __init__(self, local_path, docker_path, container_name, container_interpreter, gitHub_url, folder_ignore_list):
        self.local_path = local_path
        self.docker_path = docker_path
        self.container_name = container_name
        self.container_interpreter = container_interpreter
        self.gitHub_url = gitHub_url
        self.folder_ignore_list = ["__pycache__", ".git", ".idea", "venv", "OLD"]

    def docker_restart(self):
        DockerCmd.dockerRestart(self.container_name)

    def docker_remove_old(self):
        DockerCmd.dockerExec(
            name=self.container_name,
            cmd=f"rm -rf {self.docker_path}",
            detach=False,
            interactive=True,
            TTY=False,
        )

    def docker_clone(self):
        DockerCmd.dockerExec(
            name=self.container_name,
            cmd=f"git clone {self.gitHub_url} {self.docker_path}",
            detach=False,
            interactive=True,
            TTY=False,
        )

    def docker_mkdir(self):
        for root, dirs, files in os.walk(self.local_path):
            rootCheck = False
            for r_ in self.folder_ignore_list:
                if root.find(r_) != -1:
                    rootCheck = True
            if rootCheck:
                continue

            DockerCmd.dockerExec(
                name=self.container_name,
                cmd=f"mkdir -p {root.replace(self.local_path, self.docker_path)}",
                detach=False,
                interactive=True,
                TTY=False,
            )

    def docker_copy(self):
        for root, dirs, files in os.walk(self.local_path):
            rootCheck = False
            for r_ in self.folder_ignore_list:
                if root.find(r_) != -1:
                    rootCheck = True
            if rootCheck:
                continue

            for file in files:
                # 把現在執行的程式更新到container中
                file_name = os.path.join(root, file).replace('(', '\\(').replace(')', '\\)')
                DockerCmd.dockerCopy(
                    name=self.container_name,
                    filePath=file_name,
                    targetPath=file_name.replace(self.local_path, self.docker_path),
                )

    def ci_run(self):
        self.docker_restart()
        self.docker_remove_old()
        self.docker_clone()
        self.docker_mkdir()
        self.docker_copy()

    def cd_run(self, py_name, py_params, detach=False):
        DockerCmd.dockerExec(
            name=self.container_name,
            cmd=f'/bin/bash -c "cd {self.docker_path} && {self.container_interpreter} {py_name} {py_params}"',
            detach=detach,
            interactive=True,
            TTY=False,
        )


if __name__ == "__main__":
    pass
    # import env_config
    # # ------------------------ env_params ------------------------
    # CONTAINER_NAME = env_config.CONTAINER_PYTHON_3_8_18_NAME
    # ROOT_PATH_DOCKER = env_config.CONTAINER_PYTHON_3_8_18_PROJECT_PATH    # DOCKER 執行路徑
    # ROOT_PATH_LOCAL = env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH      # LOCAL 執行路徑
    #
    # # 重啟docker container
    # DockerCmd.dockerRestart(CONTAINER_NAME)
    #
    # # 移除container中的舊程式
    # DockerCmd.dockerExec(
    #     name=CONTAINER_NAME,
    #     cmd=f"rm -rf {ROOT_PATH_DOCKER}",
    #     detach=False,
    #     interactive=True,
    #     TTY=False,
    # )
    #
    # # 把gitHub上的程式碼clone到docker container中
    # GITHUB_URL = env_config.GITHUB_URL
    # DockerCmd.dockerExec(
    #     name=CONTAINER_NAME,
    #     cmd=f"git clone {GITHUB_URL} {ROOT_PATH_DOCKER}",
    #     detach=False,
    #     interactive=True,
    #     TTY=False,
    # )
    #
    # # CONTAINERNAME - CI
    # for root, dirs, files in os.walk(ROOT_PATH_LOCAL):
    #     rootCheck = False
    #     for r_ in ["__pycache__", ".git", ".idea", "venv", "OLD"]:
    #         if root.find(r_) != -1:
    #             rootCheck = True
    #     if rootCheck:
    #         continue
    #
    #     DockerCmd.dockerExec(
    #         name=CONTAINER_NAME,
    #         cmd=f"mkdir -p {root.replace(ROOT_PATH_LOCAL, ROOT_PATH_DOCKER)}",
    #         detach=False,
    #         interactive=True,
    #         TTY=False,
    #     )
    #
    #     for file in files:
    #         # 把現在執行的程式更新到container中
    #         file_name = os.path.join(root, file).replace('(', '\\(').replace(')', '\\)')
    #         DockerCmd.dockerCopy(
    #             name=CONTAINER_NAME,
    #             filePath=file_name,
    #             targetPath=file_name.replace(ROOT_PATH_LOCAL, ROOT_PATH_DOCKER),
    #         )


    # DockerCmd.dockerExec(
    #     name=CONTAINER_NAME,
    #     cmd=f'/bin/bash -c "cd {ROOT_PATH_DOCKER} && {DOCKER_INTERPRETER} {PY_NAME} docker_local"',
    #     detach=DEPLOY_DETACH,
    #     interactive=True,
    #     TTY=False,
    # )