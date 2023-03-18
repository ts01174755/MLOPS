import re
import pandas as pd

class PosgresParseGoogleForm():

    def __init__(self):
        pass

    # 解析爬蟲資料
    def parseGoogleFromData(self, mongoDBCtrl, collection, queryFilter, DATADATE):
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
            if dt <= DATADATE:continue

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