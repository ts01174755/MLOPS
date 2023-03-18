import os;
import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow

# load_dotenv(find_dotenv('env/.env'))



if __name__ == '__main__':
    CONTAINERNAME = 'python3.8.16'
    PROJECTNAME = 'FS_PythonServer'

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

    # FS_PythonServer - CI/CD
    for root, dirs, files in os.walk(f'/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/{PROJECTNAME}'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS', '/Users/peiyuwu/MLOPS')
            )
    for f_ in ['', '2_lineNotifyServer.py']:
        if f_ in ['']: continue
        mlflow.CD(
            containerName=CONTAINERNAME,
            interpreter='python3.8',
            targetPath=f'/Users/peiyuwu/MLOPS/{PROJECTNAME}/{f_}',
            paramArgs=f'/Users/peiyuwu/MLOPS',
        )