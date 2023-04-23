import numpy as np
import re
import pandas as pd
from src.model.mongodb import MongoDB
from src.model.postgres import PostgresDB
import time


class PosgresParseMongodbData:


    # 解析爬蟲資料
    def parseSTData(self, MONGODB, MONGODB_COLLECTION, MONGODB_QUERY, PROGRESDB_SCHEMA_DICT, DATA_TIME):

        # mongodb查詢一段時間內的資料
        rows = MONGODB.find_document(MONGODB_COLLECTION, MONGODB_QUERY)
        crawlerResText = rows[-1]["crawlerResText"]

        # 連接儲存解析後的DataBase
        reStr = re.search(r"events: \[\n\n\{.*\},    \]", crawlerResText).group(0)
        reStr = reStr.replace("events: [\n\n", "").replace(",    ]", "")
        reStrList = reStr.split("},{")
        crawlerDataList = []
        for reStr in reStrList:
            crawlerData = []
            reStr = (
                reStr.replace("{", "")
                .replace("}", "")
                .replace("title:", "")
                .replace("start:", "")
                .replace("end:", "")
            )
            reStrs = reStr.split(",")

            crawlerData.append(reStrs[-2].replace("'", ""))
            crawlerData.append(reStrs[-1].replace("'", ""))
            reStrDataList = reStrs[0].replace("'", "").split("\t")
            crawlerData.append(reStrDataList[0].replace("所屬單位：", ""))
            crawlerData.append(reStrDataList[1].replace("上課地點：", ""))
            crawlerData.append(reStrDataList[2].replace("年級：", ""))
            crawlerData.append(reStrDataList[3].replace("課程：", ""))
            crawlerData.append(reStrDataList[4].replace("老師：", ""))
            crawlerData.append(reStrDataList[5].replace("學生：", ""))
            crawlerData.append(reStrDataList[6].replace("上課日期：", ""))
            crawlerData.append(reStrDataList[7].replace("開始時間：", ""))
            crawlerData.append(reStrDataList[8].replace("結束時間：", ""))

            crawlerDataList.append(crawlerData)
        crawlerDataNumpy = np.array(crawlerDataList)
        # 資料取前８欄
        responses_df = pd.DataFrame(
            crawlerDataNumpy[:, :8],
            columns=['uniquechar1', 'uniquechar2', 'uniquechar3', 'uniquechar4',
                     'uniquechar5', 'uniquechar6', 'uniquechar7', 'uniquechar8']
        )
        responses_df["dt"] = DATA_TIME
        responses_df["memo"] = PROGRESDB_SCHEMA_DICT["memo"]
        responses_df["commondata1"] = PROGRESDB_SCHEMA_DICT["commondata1"]

        return responses_df

    def parseGoogleSTFromData(self, MONGODB, DATA_TIME, MONGODB_COLLECTION, MONGODB_QUERY, PROGRESDB_SCHEMA_DICT):
        # mongodb查詢一段時間內的資料
        rows = MONGODB.find_document(
            MONGODB_COLLECTION, MONGODB_QUERY
        )
        crawlerResText = rows[-1]["crawlerResText"]

        # 解析爬蟲資料
        keyMappping = {
            "13e6b85a": "年級",
            "0ba3adbd": "授課老師（中文姓名／英文姓名）",
            "4234b124": "上課地點",
            "6c712e8f": "課堂所屬單位",
            "6bd1afcd": "上課學生（中文姓名／英文姓名）",
            "071de1fa": "課程",
        }
        responsesDatas = crawlerResText["responses"]
        responsesDataList = []
        for d_ in responsesDatas:
            responsesDataDict = {}
            responsesDataDict["lastSubmittedTime"] = d_["lastSubmittedTime"]
            responsesDataDict["respondentEmail"] = d_["respondentEmail"]

            # dt往後8小時
            dt = time.strptime(responsesDataDict['lastSubmittedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = time.localtime(time.mktime(dt) + 8 * 60 * 60)

            # truncate_time_start 往前一天
            truncate_time_start = time.strptime(MONGODB_QUERY['dt']['$gte'], '%Y-%m-%d')
            truncate_time_start = time.localtime(time.mktime(truncate_time_start) - 1 * 60 * 60 * 24)

            # truncate_time_end 往前一天
            truncate_time_end = time.strptime(MONGODB_QUERY['dt']['$lt'], '%Y-%m-%d')
            truncate_time_end = time.localtime(time.mktime(truncate_time_end) - 1 * 60 * 60 * 24)

            if dt >= truncate_time_end or dt < truncate_time_start:
                continue

            # 依照順序將資料寫入
            for k_ in ['6c712e8f', '4234b124', '13e6b85a', '071de1fa', '0ba3adbd', '6bd1afcd']:
                tempList = []
                for ans_dict_ in d_["answers"][k_]["textAnswers"]["answers"]:
                    tempList.append(ans_dict_["value"])
                responsesDataDict[keyMappping[k_]] = ",".join(tempList)
            responsesDataList.append(responsesDataDict)
        if len(responsesDataList) == 0:
            return pd.DataFrame(responsesDataList)
        else:
            responses_df = pd.DataFrame(responsesDataList)
            responses_df = responses_df.rename(columns={
                "lastSubmittedTime": "uniquechar1",
                "respondentEmail": "uniquechar2",
                "課堂所屬單位": "uniquechar3",
                "上課地點": "uniquechar4",
                "年級": "uniquechar5",
                "課程": "uniquechar6",
                "授課老師（中文姓名／英文姓名）": "uniquechar7",
                "上課學生（中文姓名／英文姓名）": "uniquechar8",
            })
            responses_df["dt"] = DATA_TIME
            responses_df["memo"] = PROGRESDB_SCHEMA_DICT["memo"]
            responses_df["commondata1"] = PROGRESDB_SCHEMA_DICT["commondata1"]
            return responses_df

    # 將解析後的資料寫入Postgres
    def insertPostgresData(self, PROGRESDB, PROGRESDB_TABLE, PROGRESDB_SCHEMA, dataFrame):
        if dataFrame.shape[0] == 0:
            return "no data"

        # 連接儲存解析後的DataBase
        conn = PROGRESDB.connectSQLAlchemy()
        dataFrame.to_sql(
            PROGRESDB_TABLE,
            conn,
            schema=PROGRESDB_SCHEMA,
            if_exists="append",
            index=False
        )
        return "success"

    def makeDataSchema(
        self, PROGRESDB, tableName, schemaDict, schemaFilePath, columnList=None
    ):
        """以後可以把製作Table 的Schema封裝成一個工具"""
        PROGRESDB.connect()

        # 更新資料表的欄位含義
        df = PROGRESDB.queryTableSchemaDataFrame(tableName)
        df["memo"] = ""
        dfColumnNameMemo = df[["column_name", "memo"]].reset_index(drop=True)
        dfColumnNameMemo.set_index("column_name", inplace=True)
        dfColumnNameMemo = dfColumnNameMemo.T
        dfColumnNameMemoDict = dfColumnNameMemo.to_dict("records")[0]
        for k_ in schemaDict.keys():
            dfColumnNameMemoDict[k_] = schemaDict[k_]

        # 把資料表的欄位含義寫入csv
        dfColumnNameMemo = pd.DataFrame(dfColumnNameMemoDict, index=[tableName])[
            columnList
        ].transpose()

        # 把欄位順續改成原本的順序
        dfColumnNameMemo = dfColumnNameMemo
        dfColumnNameMemo.to_csv(schemaFilePath, encoding="utf_8_sig")
        return dfColumnNameMemoDict
