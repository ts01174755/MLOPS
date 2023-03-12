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
        envPATH='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/env/.env'
    )

    # env - CI
    for root, dirs, files in os.walk(f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/env'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS', '/Users/peiyuwu/MLOPS')
            )

    # package - CI
    for root, dirs, files in os.walk(f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/package'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS', '/Users/peiyuwu/MLOPS')
            )

    # mongoDB - CI/CD
    for root, dirs, files in os.walk(f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/{PROJECTNAME}'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS', '/Users/peiyuwu/MLOPS')
            )
    for f_ in ['1_mongoCreateDB.py', '2_STCrawler.py', '3_GoogleFormApi.py']:
        if f_ in ['1_mongoCreateDB.py', '2_STCrawler.py']: continue
        mlflow.CD(
            containerName=CONTAINERNAME,
            interpreter='python3.8',
            targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/{f_}',
            # paramArgs = f'/Users/peiyuwu/MLOPS st_all_data', # 正式環境
            paramArgs=f'/Users/peiyuwu/MLOPS tempdb',           # 測試環境
        )