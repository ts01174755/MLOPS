import os; import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())

from package.CICD.MLFlow import MLFlow




if __name__ == '__main__':
    CONTAINERNAME = 'mongodb'
    PROJECTNAME = 'DE_MongoDB'

    mlflow = MLFlow()
    mlflow.deploy(
        containerName=CONTAINERNAME,
        gitHubUrl='https://github.com/ts01174755/MLOPS.git',
        targetPath='/Users/ethanwu/MLOps_NS_RD', 
        envPATH='/Users/ethanwu/Documents/GitHub/MLOps_NS_RD/env/.env' 
    )

    # env - CI
    for root, dirs, files in os.walk(f'/Users/ethanwu/Documents/GitHub/MLOps_NS_RD/env/'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/ethanwu/Documents/GitHub/MLOps_NS_RD', '/Users/ethanwu/MLOps_NS_RD')
            )

    # package - CI
    for root, dirs, files in os.walk(f'/Users/ethanwu/Documents/GitHub/MLOps_NS_RD/package'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/ethanwu/Documents/GitHub/MLOps_NS_RD', '/Users/ethanwu/MLOps_NS_RD')
            )

    # mongoDB - CI/CD
    for root, dirs, files in os.walk(f'/Users/ethanwu/Documents/GitHub/MLOps_NS_RD/{PROJECTNAME}'):
        for file in files:
            if root.find('__pycache__') != -1: continue
            mlflow.CI(
                containerName=CONTAINERNAME,
                filePath=os.path.join(root, file),
                targetPath=os.path.join(root, file).replace('/Users/ethanwu/Documents/GitHub/MLOps_NS_RD', '/Users/ethanwu/MLOps_NS_RD')
            )
    for f_ in ['mongoCreateDB.py', '1_STCrawler.py', '2_GoogleFormApi.py']:
        if f_ in ['mongoCreateDB.py', '1_STCrawler.py']: continue
        mlflow.CD(
            containerName=CONTAINERNAME,
            interpreter='python3.8',
            targetPath=f'/Users/ethanwu/MLOps_NS_RD/{PROJECTNAME}/{f_}',
            paramArgs=f'/Users/ethanwu/MLOps_NS_RD', # 根目錄
        )