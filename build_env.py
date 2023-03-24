import os 
#-----------------------------------------------------------------------
# BUILD_ENV: MongoDB, MongoExpress, Mongo_PythonEnv, PostgresSQL, PostgresSQLadmin, PostgresSQL_PythonEnv
BUILD_ENV = 'PostgresSQL_PythonEnv'
# STEP: pull_image, docker_run
STEP = 'docker_run'
#-----------------------------------------------------------------------


# Run MongoDBDockerBuild.py
if __name__ == '__main__':  
    if BUILD_ENV == 'MongoDB':  
        cmd = f"python3 ./EnvironmentSetting/Docker/MongoDBDockerBuild.py {BUILD_ENV} {STEP}"
        os.system(cmd)

    if BUILD_ENV == 'MongoExpress':  
        cmd = f"python3 ./EnvironmentSetting/Docker/MongoDBDockerBuild.py {BUILD_ENV} {STEP}"
        os.system(cmd)

    if BUILD_ENV == 'Mongo_PythonEnv':  
        cmd = f"python3 ./EnvironmentSetting/Docker/MongoDBDockerBuild.py {BUILD_ENV} {STEP}"
        os.system(cmd)

    if BUILD_ENV == 'PostgresSQL':  
        cmd = f"python3 ./EnvironmentSetting/Docker/PostgresDockerBuild.py {BUILD_ENV} {STEP}"
        os.system(cmd)

    if BUILD_ENV == 'PostgresSQLadmin':  
        cmd = f"python3 ./EnvironmentSetting/Docker/PostgresDockerBuild.py {BUILD_ENV} {STEP}"
        os.system(cmd)

    if BUILD_ENV == 'PostgresSQL_PythonEnv':  
        cmd = f"python3 ./EnvironmentSetting/Docker/PostgresDockerBuild.py {BUILD_ENV} {STEP}"
        os.system(cmd)