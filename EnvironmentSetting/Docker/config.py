#-----------------------------------------------------------------------
# BUILD_ENV: MongoDB, MongoExpress, PythonEnv
BUILD_ENV = 'PythonEnv'
# STEP: pull_image, docker_run
STEP = 'docker_run'
#-----------------------------------------------------------------------


class MongoDB:
    def __init__(self):
        self.tag = 'mongo:5.0.15'
        self.name = 'mongodb'
        self.port = '27017:27017'
        self.volume = '/Users/ethanwu/Desktop/WorkSpace_tmp/mlops_dev/docker/mongodb:/Users/ethanwu'
        self.envDict = {'MONGO_INITDB_ROOT_USERNAME': 'mongodb', 'MONGO_INITDB_ROOT_PASSWORD': 'mongodb'}
        self.network = 'mongo-net'


class MongoExpress:
    def __init__(self):
        self.tag = 'mongo-express:0.54.0'
        self.name = 'mongo_express'
        self.port = '8081:8081'
        self.volume = '/Users/ethanwu/Desktop/WorkSpace_tmp/mlops_dev/docker/mongo_express:/Users/ethanwu'
        self.envDict = {'ME_CONFIG_MONGODB_SERVER': 'mongodb',
                        'ME_CONFIG_MONGODB_ADMINUSERNAME': 'mongodb',
                        'ME_CONFIG_MONGODB_ADMINPASSWORD': 'mongodb',
                        'ME_CONFIG_BASICAUTH_USERNAME': 'mongoUser', # Ui Account
                        'ME_CONFIG_BASICAUTH_PASSWORD': 'mongoUserPassword' # Ui Pwd
                        }
        self.network = 'mongo-net'


