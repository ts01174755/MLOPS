import os
import sys
import time
from dotenv import load_dotenv, find_dotenv
import subprocess
import json
load_dotenv(find_dotenv("env/.env"))

if __name__ == "__main__":
    RUN = "st_admin_course_schema_file" if len(sys.argv) == 1 else sys.argv[1]
    if RUN == "st_create_course_form":
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        PROGRESDB_TABLE = ["google_form", "tempdb"][0]
        PROGRESDB_SCHEMA = "original"
        # ---------------------- route: postgresParseMongodb -----------------------
        POST_INFO = {
            "DATA_TIME": DATA_TIME,
            "MONGODB_COLLECTION": ["google_form", "tempdb"][0],
            "MONGODB_QUERY": {
                "dt": {
                    "$gte": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                    "$lt": time.strftime(
                        "%Y-%m-%d", time.localtime(time.time() + 86400)
                    ),
                }
            },
            "PROGRESDB_SCHEMA": PROGRESDB_SCHEMA,
            "PROGRESDB_TABLE": PROGRESDB_TABLE,
            "PROGRESDB_SCHEMA_DICT": {
                "dt": "資料更新時間",
                "memo": "新申請課程",
                "commondata1": '"GoogleForm表單"',
                "uniquechar1": "填表日",
                "uniquechar2": "申請人(Email)",
                "uniquechar3": "所屬單位",
                "uniquechar4": "上課地點",
                "uniquechar5": "年級",
                "uniquechar6": "課程",
                "uniquechar7": "老師",
                "uniquechar8": "學生",
            },
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8002/PostgresDB/mongodbToProgres/stCreateCourseForm"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8002/PostgresDB/mongodbToProgres/stCreateCourseForm",
            shell=True,
        )

    elif RUN == "st_admin_course":
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        MONGODB_COLLECTION = ["st_all_data", "tempdb"][0]
        PROGRESDB_SCHEMA = "original"
        PROGRESDB_TABLE = ["st_all_data", "tempdb"][0]
        # ---------------------- route: postgresParseMongodb -----------------------
        POST_INFO = {
            "DATA_TIME": DATA_TIME,
            "MONGODB_COLLECTION": MONGODB_COLLECTION,
            "MONGODB_QUERY": {
                "dt": {
                    "$gte": time.strftime("%Y-%m-%d", time.localtime(time.time())),
                    "$lt": time.strftime(
                        "%Y-%m-%d", time.localtime(time.time() + 86400)
                    ),
                }
            },
            "PROGRESDB_SCHEMA": PROGRESDB_SCHEMA,
            "PROGRESDB_TABLE": PROGRESDB_TABLE,
            "PROGRESDB_SCHEMA_DICT": {
                "dt": "資料更新時間",
                "memo": "ST所有課程資料",
                "commondata1": '"AdminCourses"',
                "uniquechar1": "開始時間",
                "uniquechar2": "結束時間",
                "uniquechar3": "所屬單位",
                "uniquechar4": "上課地點",
                "uniquechar5": "年級",
                "uniquechar6": "課程",
                "uniquechar7": "老師",
                "uniquechar8": "學生",
                "uniquechar9": "課程",
            },
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8002/PostgresDB/mongodbToProgres/stAdminCourses"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8002/PostgresDB/mongodbToProgres/stAdminCourses",
            shell=True,
        )
    elif RUN == "st_admin_course_schema_file":
        DATA_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        DATA_DAY = time.strftime("%Y-%m-%d", time.localtime())
        MONGODB_COLLECTION = ["st_all_data", "tempdb"][0]
        PROGRESDB_SCHEMA = "original"
        PROGRESDB_TABLE = ["st_all_data", "tempdb"][0]
        # ---------------------- route: postgresParseMongodb -----------------------
        POST_INFO = {
            "PROGRESDB_TABLE": PROGRESDB_TABLE,
            "KWARGS": {
                "COLUMNS_LIST": [
                    "dt", "memo",
                    "commondata1", "commondata2", "commondata3", "commondata4", "commondata5",
                    "commondata6", "commondata7", "commondata8", "commondata9", "commondata10",
                    "uniquechar1", "uniquechar2", "uniquechar3", "uniquechar4", "uniquechar5",
                    "uniquechar6", "uniquechar7", "uniquechar8", "uniquechar9", "uniquechar10",
                    "uniqueint1", "uniqueint2", "uniqueint3", "uniqueint4", "uniqueint5",
                    "uniqueint6", "uniqueint7", "uniqueint8", "uniqueint9", "uniqueint10",
                    "uniquefloat1", "uniquefloat2", "uniquefloat3", "uniquefloat4", "uniquefloat5",
                    "uniquefloat6", "uniquefloat7", "uniquefloat8", "uniquefloat9", "uniquefloat10",
                    "uniquefloat11", "uniquefloat12", "uniquefloat13", "uniquefloat14", "uniquefloat15",
                    "uniquestring1", "uniquestring2", "uniquestring3", "uniquestring4", "uniquestring5", "uniquejason",
                ],
                "PROGRESDB_SCHEMA_FILE": f"{PROGRESDB_SCHEMA}.{PROGRESDB_TABLE}.csv",
                "PROGRESDB_SCHEMA_DICT": {
                    "dt": "資料更新時間",
                    "memo": "ST所有課程資料",
                    "commondata1": '"AdminCourses"',
                    "uniquechar1": "開始時間",
                    "uniquechar2": "結束時間",
                    "uniquechar3": "所屬單位",
                    "uniquechar4": "上課地點",
                    "uniquechar5": "年級",
                    "uniquechar6": "課程",
                    "uniquechar7": "老師",
                    "uniquechar8": "學生",
                    "uniquechar9": "課程",
                },
            },
        }
        print(
            f"\ncurl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8002/PostgresDB/mongodbToProgres/makeSchemaFile"
        )
        subprocess.run(
            f"curl -X POST -H \"Content-Type: application/json\" -d '{json.dumps(POST_INFO)}' http://localhost:8002/PostgresDB/mongodbToProgres/makeSchemaFile",
            shell=True,
        )

