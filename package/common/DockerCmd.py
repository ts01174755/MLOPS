from package.common.shellCmd import shellCmd

class DockerFileSystem:
    def __init__(self):
        self.shellcmd = shellCmd()

    def dockerWrite(self, name, path, data):
        # 把資料寫入docker container
        print(f"docker exec -i {name} /bin/bash -c 'echo {data} > {path}'")
        self.shellcmd.execute(f"docker exec -i {name} /bin/bash -c 'echo -e \"{data}\" > {path}'", shell=True)

class DockerContainer:
    def __init__(self):
        self.shellcmd = shellCmd()

    def dockerRun(self, tag, name, port, volume, envDict = {}, detach=True, interactive=True, TTY=False): # 建立docker container
        env = ""
        for key, value in envDict.items(): env += f"-e {key}={value} "
        par = "-" if interactive | detach | TTY else ""
        par += "i" if interactive else ""
        par += "d" if detach else ""
        par += "t" if TTY else ""
        print(f"docker run --name {name} -p {port} -v {volume} {env}{par} {tag}")
        self.shellcmd.execute(f"docker run --name {name} -p {port} -v {volume} {env}{par} {tag}",shell=True)

    def dockerCreate(self, tag, name, port, volume):  # 建立docker container
        print(f"docker create --name {name} -p {port} -v {volume} {tag}")
        self.shellcmd.execute(f"docker create --name {name} -p {port} -v {volume} {tag}", shell=True)

    def dockerRemove(self, name):  # 刪除docker container
        print(f"docker rm {name}")
        self.shellcmd.execute(f"docker rm {name}", shell=True)

    def dockerStart(self, name):  # 啟動docker container
        print(f"docker start {name}")
        self.shellcmd.execute(f"docker start {name}", shell=True)

    def dockerStop(self, name):  # 停止docker container
        print(f"docker stop {name}")
        self.shellcmd.execute(f"docker stop {name}", shell=True)

    def dockerExec(self, name, cmd, detach=True, interactive=False, TTY=False):  # 執行docker container的指令
        par = "-" if interactive | detach | TTY else ""
        par += "i" if interactive else ""
        par += "d" if detach else ""
        par += "t" if TTY else ""
        print(f"docker exec {par} {name} {cmd}")
        self.shellcmd.execute(f"docker exec {par} {name} {cmd}", shell=True)

    def dockerPs(self): # 查看docker container
        print("docker ps -a")
        self.shellcmd.execute("docker ps -a", shell=True)

    def dockerLogs(self, name): # 查看docker container的log
        print(f"docker logs {name}")
        self.shellcmd.execute(f"docker logs {name}", shell=True)

    def dockerInspect(self, name): # 查看docker container的詳細資訊，並回傳成Jason格式
        print(f"docker inspect {name}")
        return self.shellcmd.getoutput(f"docker inspect {name}")

class DockerImage:
    def __init__(self):
        self.shellcmd = shellCmd()

    def dockerPull(self, tag): # 從docker hub下載image
        print(f"docker push {tag}")
        self.shellcmd.execute(f"docker pull {tag}", shell=True)

    def dockerBuild(self, dockerfile, tag): # 建立docker image
        print(f"docker build -f {dockerfile} -t {tag} .")
        self.shellcmd.execute(f"docker build -f {dockerfile} -t {tag} .", shell=True)

    def dockerTag(self, tag, newTag): # 重新命名image
        print(f"docker tag {tag} {newTag}")
        self.shellcmd.execute(f"docker tag {tag} {newTag}", shell=True)

    def dockerSave(self, tag, path): # 儲存image
        print(f"docker save {tag} -o {path}")
        self.shellcmd.execute(f"docker save {tag} -o {path}", shell=True)

    def dockerLoad(self, path): # 載入image
        print(f"docker load -i {path}")
        self.shellcmd.execute(f"docker load -i {path}", shell=True)
    def dockerPush(self, tag): # 上傳image到docker hub
        print(f"docker push {tag}")
        self.shellcmd.execute(f"docker push {tag}", shell=True)

    def dockerRmi(self, tag): # 刪除docker image
        print(f"docker rmi {tag}")
        self.shellcmd.execute(f"docker rmi {tag}", shell=True)

    def dockerImages(self): # 查看docker image
        print("docker images")
        self.shellcmd.execute("docker images", shell=True)

# 將docker的操作進行封裝
class DockerCmd(DockerFileSystem, DockerContainer, DockerImage):
    def __init__(self):
        self.shellcmd = shellCmd()

    def dockerLogin(self, username, password): # 登入docker hub
        print(f"docker login -u {username} -p {password}")
        self.shellcmd.execute(f"docker login -u {username} -p {password}", shell=True)



