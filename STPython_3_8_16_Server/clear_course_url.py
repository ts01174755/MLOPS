from contorller.clear_course_url import ClearCourseUrl
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

if __name__ == '__main__':
    QUERFILTER = {
        'from': 'init_course_collection',
        'dt': '2023-05-10 21:16:44'
    }
    PROGRESDB_SCHEMA_DICT = {
        "dt": "資料更新時間",
        "memo": "課程規劃",
        "commondata1": "產品名",
        "uniquechar1": "影片連結"
    }
    data_clear = ClearCourseUrl()
    data_clear.clear_course_url(MONGODB, POSTGRESDB, QUERFILTER, PROGRESDB_SCHEMA_DICT)