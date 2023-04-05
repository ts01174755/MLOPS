import pandas as pd
from src.my_model.mongodb import MongoDB
from src.my_model.postgres import PostgresDB
import time

class PosgresParseMongodbData():
    def parseGoogleFromData(self, MONGODB_INFO):
        mongodb = MongoDB(
            user_name=MONGODB_INFO['MONGODB_USER'],
            user_password=MONGODB_INFO['MONGODB_PASSWORD'],
            host=MONGODB_INFO['MONGODB_HOST'], # 這個是用來連接內部的MongoDB(內部連接)
            port=MONGODB_INFO['MONGODB_PORT'],
            database_name=MONGODB_INFO['MONGODB_DATABASE'],
        )

        # mongodb查詢一段時間內的資料
        rows = mongodb.find_document(MONGODB_INFO['MONGODB_COLLECTION'], MONGODB_INFO['MONGODB_QUERY'])
        crawlerResText = rows[-1]['crawlerResText']

        # 解析爬蟲資料
        keyMappping = {
            '13e6b85a': '年級',
            '0ba3adbd': '授課老師（中文姓名／英文姓名）',
            '4234b124': '上課地點',
            '6c712e8f': '課堂所屬單位',
            '6bd1afcd': '上課學生（中文姓名／英文姓名）',
            '071de1fa': '課程',
        }
        responsesDatas = crawlerResText['responses']
        responsesDataList = []
        for d_ in responsesDatas:
            responsesDataDict = {}
            responsesDataDict['lastSubmittedTime'] = d_['lastSubmittedTime']
            responsesDataDict['respondentEmail'] = d_['respondentEmail']

            # dt往後8小時
            dt = time.strptime(responsesDataDict['lastSubmittedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = time.localtime(time.mktime(dt) + 8 * 60 * 60)

            # truncate_time_start 往前一天
            truncate_time_start = time.strptime(MONGODB_INFO['MONGODB_QUERY']['dt']['$gte'], '%Y-%m-%d')
            truncate_time_start = time.localtime(time.mktime(truncate_time_start) - 1 * 60 * 60 * 24)

            # truncate_time_end 往前一天
            truncate_time_end = time.strptime(MONGODB_INFO['MONGODB_QUERY']['dt']['$lt'], '%Y-%m-%d')
            truncate_time_end = time.localtime(time.mktime(truncate_time_end) - 1 * 60 * 60 * 24)

            if dt >= truncate_time_end or dt < truncate_time_start:
                continue

            # 依照順序將資料寫入
            for k_ in ['6c712e8f', '4234b124', '13e6b85a', '071de1fa', '0ba3adbd', '6bd1afcd']:
                tempList = []
                for ans_dict_ in d_['answers'][k_]['textAnswers']['answers']:
                    tempList.append(ans_dict_['value'])
                responsesDataDict[keyMappping[k_]] = ','.join(tempList)
            responsesDataList.append(responsesDataDict)
        if len(responsesDataList) == 0:
            return pd.DataFrame(responsesDataList)
        else:
            df = pd.DataFrame(responsesDataList)
            df = df[['lastSubmittedTime', 'respondentEmail', '課堂所屬單位', '上課地點', '年級', '課程', '授課老師（中文姓名／英文姓名）', '上課學生（中文姓名／英文姓名）']]
            return df

    # 將解析後的資料寫入Postgres
    def insertGoogleFromData(self, PROGRESDB_INFO, dataNumpy, dt):
        if dataNumpy.shape[0] == 0: return 'no data'

        # 連接postgres
        postgres = PostgresDB(
            user=PROGRESDB_INFO['POSTGRES_USER'],
            password=PROGRESDB_INFO['POSTGRES_PASSWORD'],
            host=PROGRESDB_INFO['POSTGRES_HOST'],
            database=PROGRESDB_INFO['POSTGRES_DATABASE'],
        )

        # 連接儲存解析後的DataBase
        postgres.connect()

        # 資料寫入 original.st_all_data
        for data_ in dataNumpy:
            insertDataStr = "\',\'".join(data_)
            postgres.execute(f"\
            INSERT INTO original.{PROGRESDB_INFO['PROGRESDB_TABLE']} (\
                dt, memo, \
                commondata1, \
                uniquechar1, uniquechar2, uniquechar3, uniquechar4, uniquechar5, uniquechar6, uniquechar7, uniquechar8\
            ) \
            VALUES (\
                '{dt}', '新申請課程', \
                'GoogleForm表單', \
                '{insertDataStr}'\
            );")  # 插入資料
        postgres.close()

        return 'success'

    def makeInsertGoogleFromDataSchema(self, PROGRESDB_INFO, tableName, schemaDict, schemaFilePath, columnList=None):
        '''以後可以把製作Table 的Schema封裝成一個工具'''
        # 連接postgres
        postgres = PostgresDB(
            user=PROGRESDB_INFO['POSTGRES_USER'],
            password=PROGRESDB_INFO['POSTGRES_PASSWORD'],
            host=PROGRESDB_INFO['POSTGRES_HOST'],
            database=PROGRESDB_INFO['POSTGRES_DATABASE'],
        )
        postgres.connect()

        # 更新資料表的欄位含義
        df = postgres.queryTableSchemaDataFrame(tableName)
        df['memo'] = ''
        dfColumnNameMemo = df[['column_name', 'memo']].reset_index(drop=True)
        dfColumnNameMemo.set_index('column_name', inplace=True)
        dfColumnNameMemo = dfColumnNameMemo.T
        dfColumnNameMemoDict = dfColumnNameMemo.to_dict('records')[0]

        for k_ in schemaDict.keys():
            dfColumnNameMemoDict[k_] = schemaDict[k_]

        # 把資料表的欄位含義寫入csv
        dfColumnNameMemo = pd.DataFrame(dfColumnNameMemoDict, index=[tableName])[columnList].transpose()

        # 把欄位順續改成原本的順序
        dfColumnNameMemo = dfColumnNameMemo
        dfColumnNameMemo.to_csv(schemaFilePath, encoding='utf_8_sig')
        return dfColumnNameMemoDict
