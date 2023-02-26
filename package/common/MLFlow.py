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

    def dockerDeploy(self, containerName, gitHubUrl, targetPath, envObj, envKeys): # 把gitHub上的程式碼clone到docker container中
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
        # 建立一個.env檔案，寫入一行"ROLE=containerName"
        # 在TargetPath中建立一個.env檔案，寫入一行"ROLE=containerName"
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'bash -c \'echo "ROLE={containerName}" > {targetPath}/env/.env\'',
            detach=False,
            interactive=True,
            TTY=False,
        )
        for key_ in envObj:
            if key_ in envKeys:
                dockerCmd.dockerExec(
                    name=containerName,
                    cmd=f'bash -c \'echo "{key_}={envObj[key_]}" >> {targetPath}/env/.env\'',
                    detach=False,
                    interactive=True,
                    TTY=False,
                )

    def dockerCI(self, containerName, filePath, targetPath): # 把現在執行的程式更新到container中
        dockerCmd = DockerCmd()
        # 把現在執行的程式更新到container中
        dockerCmd.dockerCopy(
            name=containerName,
            filePath = filePath,
            targetPath = targetPath
        )

    def dockerCD(self, containerName, interpreter, targetPath, paramArgs):
        dockerCmd = DockerCmd()
        # 執行container中的程式
        dockerCmd.dockerExec(
            name=containerName,
            cmd=f'{interpreter} {targetPath} {paramArgs}',
            detach=False,
            interactive=True,
            TTY=False,
        )
