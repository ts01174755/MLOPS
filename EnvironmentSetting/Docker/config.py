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


class PostgresSQL:
    def __init__(self):
        self.tag = 'postgres:15.2'
        self.name = 'postgres15.2'
        self.port = '5432:5432'
        self.volume = '/Users/ethanwu/Desktop/WorkSpace_tmp/mlops_dev/docker/postgres15.2:/Users/ethanwu'
        self.envDict = {'POSTGRES_USER': 'postgres', 'POSTGRES_PASSWORD': 'postgres', 'POSTGRES_DB': 'postgres'}


class PostgresSQLadmin:
    def __init__(self):
        self.tag = 'dpage/pgadmin4:6.20'
        self.name = 'pgadmin4'
        self.port = '5050:80'
        self.volume = '/Users/ethanwu/Desktop/WorkSpace_tmp/mlops_dev/docker/pgadmin4:/Users/ethanwu'
        self.envDict = {'PGADMIN_DEFAULT_EMAIL': 'pgadmin4@gmail.com', 'PGADMIN_DEFAULT_PASSWORD': 'pgadmin4'}

# PostgresSQLadmin 執行:
# docker run -p 5050:80 \
#     -e "PGADMIN_DEFAULT_EMAIL=pgadmin4@gmail.com" \
#     -e "PGADMIN_DEFAULT_PASSWORD=pgadmin4" \
#     -d dpage/pgadmin4:6.20
#     -n pgadmin4
