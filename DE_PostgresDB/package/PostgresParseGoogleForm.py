import re
import pandas as pd

class PosgresParseGoogleForm():

    def __init__(self):
        pass

    # 解析爬蟲資料
    def parseGoogleFromData(self, mongoDBCtrl, collection, queryFilter, TODAY):
        '''以後可以把googleForm封裝成一個工具'''
        import time
        # mongodb查詢一段時間內的資料
        rows = mongoDBCtrl.find_document(collection, queryFilter)
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

            dt = time.strptime(responsesDataDict['lastSubmittedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if time.strftime('%Y-%m-%d', dt) != TODAY:continue

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
    def insertGoogleFromData(self, postgresCtrl, table, dataNumpy, dt):
        if dataNumpy.shape[0] == 0: return 'no data'

        # 連接儲存解析後的DataBase
        postgresCtrl.connect()

        # 資料寫入 original.st_all_data
        for data_ in dataNumpy:
            insertDataStr = "\',\'".join(data_)
            postgresCtrl.execute(f"\
            INSERT INTO original.{table} (\
                dt, memo, \
                commondata1, \
                uniquechar1, uniquechar2, uniquechar3, uniquechar4, uniquechar5, uniquechar6, uniquechar7, uniquechar8\
            ) \
            VALUES (\
                '{dt}', '新申請課程', \
                'GoogleForm表單', \
                '{insertDataStr}'\
            );")  # 插入資料
        postgresCtrl.close()

        return 'success'

    def makeInsertGoogleFromDataSchema(self, postgresCtrl, tableName, schemaDict, schemaFilePath, columnList=None):
        '''以後可以把製作Table 的Schema封裝成一個工具'''
        postgresCtrl.connect()

        # 更新資料表的欄位含義
        df = postgresCtrl.queryTableSchemaDataFrame(tableName)
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

if __name__ == '__main__':
    pass
    # import os;import sys;
    # from dotenv import load_dotenv, find_dotenv
    # from package.controller.PostgresCtrl import PostgresCtrl
    # import pprint
    #
    # load_dotenv(find_dotenv('env/.env'))
    #
    # # 連接PostgresDB與寫入資料
    # dfColumnNameMemoDict = PostgresParseSTData().makeInsertSTDataSchema(
    #     postgresCtrl=PostgresCtrl(
    #         host=os.getenv('POSTGRES_HOST'),
    #         user=os.getenv('POSTGRES_USER'),
    #         password=os.getenv('POSTGRES_PASSWORD'),
    #         database='originaldb'
    #     ),
    #     tableName="st_all_data",
    #     schemaDict={
    #         'dt': '資料更新時間',
    #         'memo': 'ST所有課程資料',
    #         'commondata1': '"AdminCourses"',
    #         'uniquechar1': '開始時間',
    #         'uniquechar2': '結束時間',
    #         'uniquechar3': '所屬單位',
    #         'uniquechar4': '上課地點',
    #         'uniquechar5': '年級',
    #         'uniquechar6': '課程',
    #         'uniquechar7': '老師',
    #         'uniquechar8': '學生'
    #     },
    #     schemaFilePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/DE_PostgresDB/file/STAllDataSchema.csv',
    #     columnList=[
    #         'dt', 'memo', 'commondata1', 'commondata2', 'commondata3', 'commondata4', 'commondata5',
    #         'commondata6', 'commondata7', 'commondata8', 'commondata9', 'commondata10', 'uniquechar1',
    #         'uniquechar2', 'uniquechar3', 'uniquechar4', 'uniquechar5', 'uniquechar6', 'uniquechar7',
    #         'uniquechar8', 'uniquechar9', 'uniquechar10', 'uniqueint1', 'uniqueint2', 'uniqueint3',
    #         'uniqueint4', 'uniqueint5', 'uniqueint6', 'uniqueint7', 'uniqueint8', 'uniqueint9',
    #         'uniqueint10', 'uniquefloat1', 'uniquefloat2', 'uniquefloat3', 'uniquefloat4', 'uniquefloat5',
    #         'uniquefloat6', 'uniquefloat7', 'uniquefloat8', 'uniquefloat9', 'uniquefloat10', 'uniquefloat11',
    #         'uniquefloat12', 'uniquefloat13', 'uniquefloat14', 'uniquefloat15', 'uniquestring1',
    #         'uniquestring2', 'uniquestring3', 'uniquestring4', 'uniquestring5', 'uniquejason'
    #     ]
    # )
    # print(dfColumnNameMemoDict)
