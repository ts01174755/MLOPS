import os;
from package.CICD.MLFlow import MLFlow



if __name__ == '__main__':
    CONTAINERNAME = 'mongodb'
    PROJECTNAME = 'DE_MongoDB'

    mlflow = MLFlow()
    mlflow.deploy(
        containerName=CONTAINERNAME,
        gitHubUrl='https://github.com/ts01174755/MLOPS.git',
        targetPath='/Users/peiyuwu/MLOPS',
    )

    # CONTAINERNAME - CI
    for root, dirs, files in os.walk(f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS'):
        rootCheck = False
        for r_ in ['__pycache__', '.git', '.idea', 'venv', 'OLD']:
            if root.find(r_) != -1: rootCheck = True
        if rootCheck: continue

        mlflow.CI_mkdir(
            containerName=CONTAINERNAME,
            targetPath=root.replace('/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS', '/Users/peiyuwu/MLOPS'),
        )
        for file in files:
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS', '/Users/peiyuwu/MLOPS')
            )

    # CONTAINERNAME - CD
    for f_ in ['mongoCreateDB.py', '1_STCrawler.py', '2_GoogleFormApi.py', '3_FuturesExchange.py']:
        if f_ in ['mongoCreateDB.py', '1_STCrawler.py', '2_GoogleFormApi.py']: continue
        mlflow.CD(
            containerName=CONTAINERNAME,
            interpreter='python3.8',
            targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/{f_}',
            paramArgs=f'/Users/peiyuwu/MLOPS',
        )