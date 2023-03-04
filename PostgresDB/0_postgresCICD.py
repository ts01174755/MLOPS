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
        containerName='postgres15.2',
        gitHubUrl='https://github.com/ts01174755/MLOPS.git',
        targetPath='/Users/peiyuwu/MLOPS',
        envPATH='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/env/.env'
    )

    # 用dockerCI()把現在執行的程式更新到container中
    mlflow.CI(
        containerName='postgres15.2',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/PostgresDB/0_postgresCICD.py',
        targetPath='/Users/peiyuwu/MLOPS/PostgresDB/0_postgresCICD.py',
    )

    mlflow.CI(
        containerName='postgres15.2',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/PostgresDB/1_postgresCreateDB.py',
        targetPath='/Users/peiyuwu/MLOPS/PostgresDB/1_postgresCreateDB.py',
    )

    # 用dockerCD()在container中執行程式
    mlflow.CD(
        containerName='postgres15.2',
        interpreter='python3.9',
        targetPath='/Users/peiyuwu/MLOPS/PostgresDB/1_postgresCreateDB.py',
        paramArgs=f'/Users/peiyuwu/MLOPS'
    )
