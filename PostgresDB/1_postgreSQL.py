import os; os.chdir(os.path.dirname(os.path.abspath(__file__)).split('PostgresDB')[0])
import sys; sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from dotenv import load_dotenv, find_dotenv


# load_dotenv(find_dotenv('../env/.env'))

if __name__ == '__main__':
    # 用工廠模式派生多個機器學習流程
    mlflow = MLFlow()

    mlflow.dockerDeploy(
        containerName='postgres15.2',
        gitHubUrl='https://github.com/ts01174755/MLOPS.git',
        targetPath='/Users/peiyuwu/MLOPS',
    )

    mlflow.dockerCIUpdate(
        containerName='postgres15.2',
        filePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/PostgresDB/1_postgreSQL.py',
        targetPath='/Users/peiyuwu/MLOPS/PostgresDB/1_postgreSQL.py',
    )
