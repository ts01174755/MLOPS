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
    CONTAINERNAME = 'mongodb'
    PROJECTNAME = 'DE_MongoDB'

    mlflow = MLFlow()
    # 用dockerDeploy()把gitHub上的程式碼clone到docker container中
    mlflow.deploy(
        containerName=CONTAINERNAME,
        gitHubUrl='https://github.com/ts01174755/MLOPS.git',
        targetPath='/Users/peiyuwu/MLOPS',
        envPATH='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/env/.env'
    )

    # 用dockerCI()把現在執行的程式更新到container中
    # package/common - CI
    for f_ in ['BS4Crawler.py', 'DatabaseCtrl.py', 'DockerCmd.py', 'MLFlow.py']:
        mlflow.CI(
            containerName=CONTAINERNAME,
            filePath=f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/package/common/{f_}',
            targetPath=f'/Users/peiyuwu/MLOPS/package/common/{f_}',
        )

    # mongoDB - CI
    # main
    for f_ in ['0_mongoCICD.py', '1_mongoCreateDB.py', '2_STCrawler.py']:
        mlflow.CI(
            containerName=CONTAINERNAME,
            filePath=f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/{PROJECTNAME}/{f_}',
            targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/{f_}',
        )

    # package
    for f_ in ['STCrawler.py']:
        mlflow.CI(
            containerName=CONTAINERNAME,
            filePath=f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/{PROJECTNAME}/package/{f_}',
            targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/package/{f_}',
        )

    # 用dockerCD()在container中執行程式
    # FILENAME = '1_mongoCreateDB.py'
    # mlflow.CD(
    #     containerName=CONTAINERNAME,
    #     interpreter='python3.8',
    #     targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/{FILENAME}',
    #     paramArgs=f'/Users/peiyuwu/MLOPS'
    # )

    FILENAME = '2_STCrawler.py'
    mlflow.CD(
        containerName=CONTAINERNAME,
        interpreter='python3.8',
        targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/{FILENAME}',
        paramArgs=f'/Users/peiyuwu/MLOPS'
    )