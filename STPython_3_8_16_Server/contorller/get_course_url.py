import pandas as pd



class GetCourseUrl():
    def __init__(self):
        pass

    def get_course_url(self, POSTGRESDB, QUERY_SQL):
        # 連接儲存解析後的DataBase
        conn = POSTGRESDB.connectSQLAlchemy().connect()
        query = QUERY_SQL.replace('"', "'")

        # 撈取資料
        df = pd.read_sql(POSTGRESDB.getSQLText(query), conn)
        df.set_index('uniquechar1', inplace=True)

        # 每個index 一個dict
        return df.to_dict('index')

if __name__ == '__main__':
    pass
    import sys
    import env_config

    RUN = "docker" if len(sys.argv) == 1 else sys.argv[1]
    RUN = "local"

    MONGODB = env_config.MONGODB_DOCKER if RUN.find('docker') != -1 else env_config.MONGODB_LOCAL  # mongodb連線資訊
    POSTGRESDB = env_config.POSTGRESDB_DOCKER if RUN.find('docker') != -1 else env_config.POSTGRESDB_LOCAL  # postgres連線資訊
    PROJECT_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH  # 存放資料的位置
    FILE_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_FILE_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_FILE_PATH  # 存放資料的位置
    DOWNLOAD_PATH = env_config.CONTAINER_PYTHON_3_8_18_SERVER_DOWNLOAD_PATH if RUN.find('docker') != -1 else env_config.MLOPS_ROOT_PATH_LOCAL_DOWNLOAD_PATH  # 存放資料的位置
    LOG_PATH = f"{env_config.CONTAINER_PYTHON_3_8_18_SERVER_PROJECT_PATH}/server_st_log.log" if RUN.find('docker') != -1 else f"{env_config.MLOPS_ROOT_PATH_LOCAL_PROJECT_PATH}/server_st_log.log"  # 執行的程式

    user_id = {
        '陳宥勳': 'stpeteam_student_00000001'
    }
    user_status = {
        'stpeteam_student_00000001': {
            # 觀看課程權限
            'course': [
                [2287, '2023/06/01', '2023/06/30', '', '', '', ''],
                [2288, '2023/06/01', '2023/06/30', '', '', '', ''],
                [2289, '2023/06/03', '2023/06/10', '', '', '', ''],
                [2290, '2023/06/03', '2023/06/10', '', '', '', ''],
                [2291, '2023/06/03', '2023/06/10', '', '', '', ''],
                [2292, '2023/06/03', '2023/06/10', '', '', '', ''],
                [2293, '2023/06/03', '2023/06/10', '', '', '', ''],
                [2294, '2023/06/10', '2023/06/17', '', '', '', ''],
                [2295, '2023/06/10', '2023/06/17', '', '', '', ''],
                [2296, '2023/06/10', '2023/06/17', '', '', '', ''],
                [2297, '2023/06/10', '2023/06/17', '', '', '', ''],
                [2298, '2023/06/10', '2023/06/17', '', '', '', ''],
                [2299, '2023/06/17', '2023/06/24', '', '', '', ''],
                [2300, '2023/06/17', '2023/06/24', '', '', '', ''],
                [2301, '2023/06/17', '2023/06/24', '', '', '', ''],
                [2302, '2023/06/24', '2023/06/30', '', '', '', ''],
                [2303, '2023/06/24', '2023/06/30', '', '', '', ''],
                [2304, '2023/06/24', '2023/06/30', '', '', '', ''],
                [2305, '2023/06/24', '2023/06/30', '', '', '', ''],
                [2306, '2023/06/24', '2023/06/30', '', '', '', ''],
            ]
        }
    }
    query = f'SELECT * FROM original.course_url'

    data_get = GetCourseUrl()
    df = data_get.get_course_url(POSTGRESDB, query)

    for _user in user_status.keys():
        for _course in user_status[_user]['course']:
            _course[3] = df[_course[0]]['uniquechar2']
            _course[4] = df[_course[0]]['uniquechar3']
            _course[5] = df[_course[0]]['uniquechar4']
            _course[6] = df[_course[0]]['uniquestring1']

    print(user_status)