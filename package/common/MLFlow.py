import time
from package.common.DockerCmd import DockerCmd

class dataFlow(object):
    def __init__(self):
        pass
    @classmethod
    def dataflow(cls, flowFunction, **kwargs):
        # 將args和kwargs分開
        args = kwargs['args']
        del kwargs['args']

        # 紀錄當今時間(年月日時分秒)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 計算程式執行時間
        start = time.time()

        # 印出function名稱
        dataFlowAction = kwargs['dataFlowAction'] if 'dataFlowAction' in kwargs else 'dataFlowAction'
        dataFlowCommit = kwargs['dataFlowCommit'] if 'dataFlowCommit' in kwargs else 'dataFlowCommit'
        print(f'Time:{now}, dataFlowAction:{dataFlowAction}, dataFlowCommit:{dataFlowCommit}, '
              f'start run function:{flowFunction.__name__}...')
        obj = flowFunction(*args, **kwargs)

        # 計算程式執行時間
        end = time.time()
        hour = int((end - start) / 3600)
        min = int((end - start) / 60)
        sec = int((end - start) % 60)
        print(f'Time:{now}, end run function:{flowFunction.__name__}')
        print(f'time cost: {hour}h {min}m {sec}s\n')
        return obj

# 用工廠模式派生多個機器學習流程
class MLFlow(object):
    def __init__(self, mlFlowObject=None):
        self.mlFlowObject = mlFlowObject
        self.dockerdeploy = False

    def __getattr__(self, name):
        def func_(*args, **kwargs): # 這裡的*args, **kwargs是為了接收dataFlow.dataflow()的參數
            kwargs['args'] = args
            return dataFlow.dataflow(flowFunction = getattr(self.mlFlowObject, name), **kwargs)
        return func_

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def deploy(self, containerName, gitHubUrl, targetPath, envPATH): # 把gitHub上的程式碼clone到docker container中
        self.dockerdeploy = True

        # 把gitHub上的程式碼clone到docker container中
        dockerCmd = DockerCmd()

        # 移除container中的舊程式
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'rm -rf {targetPath}',
            detach=False,
            interactive=True,
            TTY=False,
        )

        # 把gitHub上的程式碼clone到docker container中
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'git clone {gitHubUrl} {targetPath}',
            detach=False,
            interactive=True,
            TTY=False,
        )
        # 建立一個env資料夾
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'mkdir -p {"/".join(envPATH.split("/")[:-1])}',
            detach=False,
            interactive=True,
            TTY=False,
        )
        # 複製.env檔案到container中
        # 並寫入一行"ROLE=containerName"的設定
        dockerCmd.dockerCopy(
            name=containerName,
            filePath = envPATH,
            targetPath = targetPath
        )
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'echo "ROLE={containerName}" > {envPATH}',
            detach=False,
            interactive=True,
            TTY=False,
        )


    def CI(self, containerName, filePath, targetPath): # 把現在執行的程式更新到container中
        dockerCmd = DockerCmd()
        # 把現在執行的程式更新到container中
        dockerCmd.dockerCopy(
            name=containerName,
            filePath = filePath,
            targetPath = targetPath
        )

    def CD(self, containerName, interpreter, targetPath, paramArgs):
        dockerCmd = DockerCmd()
        # 執行container中的程式
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'{interpreter} {targetPath} {paramArgs}',
            detach=False,
            interactive=True,
            TTY=False,
        )
