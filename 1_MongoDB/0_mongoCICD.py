import os;
import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv('env/.env'))



if __name__ == '__main__':


    mlflow = MLFlow()
    # 用dockerDeploy()把gitHub上的程式碼clone到docker container中
    mlflow.deploy(
        containerName='mongodb',
        gitHubUrl='https://github.com/ts01174755/MLOPS.git',
        targetPath='/Users/peiyuwu/MLOPS',
        envPATH='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/env/.env'
    )

    # 用dockerCI()把現在執行的程式更新到container中
    # package/common - CI
    mlflow.CI(
        containerName='mongodb',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/package/common/DatabaseCtrl.py',
        targetPath='/Users/peiyuwu/MLOPS/package/common/DatabaseCtrl.py',
    )
    mlflow.CI(
        containerName='mongodb',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/package/common/DockerCmd.py',
        targetPath='/Users/peiyuwu/MLOPS/package/common/DockerCmd.py',
    )
    mlflow.CI(
        containerName='mongodb',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/package/common/MLFlow.py',
        targetPath='/Users/peiyuwu/MLOPS/package/common/MLFlow.py',
    )

    # mongoDB - CI
    mlflow.CI(
        containerName='mongodb',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/1_MongoDB/0_mongoCICD.py',
        targetPath='/Users/peiyuwu/MLOPS/1_MongoDB/0_mongoCICD.py',
    )

    mlflow.CI(
        containerName='mongodb',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/1_MongoDB/1_mongoCreateDB.py',
        targetPath='/Users/peiyuwu/MLOPS/1_MongoDB/1_mongoCreateDB.py',
    )

    # 用dockerCD()在container中執行程式
    mlflow.CD(
        containerName='mongodb',
        interpreter='python3.8',
        targetPath='/Users/peiyuwu/MLOPS/1_MongoDB/1_mongoCreateDB.py',
        paramArgs=f'/Users/peiyuwu/MLOPS'
    )
