import re
import pandas as pd

class PostgresParseSTData():

    def __init__(self):
        pass

    # 解析爬蟲資料
    def parseSTData(self, mongoDBCtrl, collection, queryFilter):
        # mongodb查詢一段時間內的資料
        rows = mongoDBCtrl.find_document(collection, queryFilter)
        crawlerResText = rows[-1]['crawlerResText']

        # 連接儲存解析後的DataBase
        reStr = re.search(r'events: \[\n\n\{.*\},    \]', crawlerResText).group(0)
        reStr = reStr.replace('events: [\n\n', '').replace(',    ]', '')
        reStrList = reStr.split('},{')
        crawlerDataList = []
        for reStr in reStrList:
            crawlerData = []
            reStr = reStr.replace('{', '').replace('}', '').replace('title:', '').replace('start:', '').replace('end:', '')
            reStrs = reStr.split(',')

            crawlerData.append(reStrs[-2].replace('\'', ''))
            crawlerData.append(reStrs[-1].replace('\'', ''))
            reStrDataList = reStrs[0].replace("\'", "").split('\t')
            crawlerData.append(reStrDataList[0].replace('所屬單位：', ''))
            crawlerData.append(reStrDataList[1].replace('上課地點：', ''))
            crawlerData.append(reStrDataList[2].replace('年級：', ''))
            crawlerData.append(reStrDataList[3].replace('課程：', ''))
            crawlerData.append(reStrDataList[4].replace('老師：', ''))
            crawlerData.append(reStrDataList[5].replace('學生：', ''))
            crawlerData.append(reStrDataList[6].replace('上課日期：', ''))
            crawlerData.append(reStrDataList[7].replace('開始時間：', ''))
            crawlerData.append(reStrDataList[8].replace('結束時間：', ''))

            crawlerDataList.append(crawlerData)

        return crawlerDataList

    # 將解析後的資料寫入Postgres
    def insertSTData(self, postgresCtrl, table, dataList, dt):
        # 連接儲存解析後的DataBase
        postgresCtrl.connect()

        # 資料寫入 original.st_all_data
        for data_ in dataList:
            postgresCtrl.execute(f"\
            INSERT INTO original.{table} (\
                dt, memo, \
                commondata1, \
                uniquechar1, uniquechar2, uniquechar3, uniquechar4, uniquechar5, uniquechar6, uniquechar7, uniquechar8\
            ) \
            VALUES (\
                '{dt}', 'ST所有課程資料', \
                'AdminCourses', \
                '{data_[0]}', '{data_[1]}', '{data_[2]}', '{data_[3]}', '{data_[4]}', '{data_[5]}', '{data_[6]}', '{data_[7]}'\
            );")  # 插入資料
        postgresCtrl.close()

        return 'success'

    def makeInsertSTDataSchema(self, postgresCtrl, tableName, schemaDict, schemaFilePath, columnList=None):
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
    import os;import sys;
    from dotenv import load_dotenv, find_dotenv
    from package.controller.PostgresCtrl import PostgresCtrl
    import pprint

    load_dotenv(find_dotenv('env/.env'))

    # 連接PostgresDB與寫入資料
    dfColumnNameMemoDict = PostgresParseSTData().makeInsertSTDataSchema(
        postgresCtrl=PostgresCtrl(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='originaldb'
        ),
        tableName="st_all_data",
        schemaDict={
            'dt': '資料更新時間',
            'memo': 'ST所有課程資料',
            'commondata1': '"AdminCourses"',
            'uniquechar1': '開始時間',
            'uniquechar2': '結束時間',
            'uniquechar3': '所屬單位',
            'uniquechar4': '上課地點',
            'uniquechar5': '年級',
            'uniquechar6': '課程',
            'uniquechar7': '老師',
            'uniquechar8': '學生'
        },
        schemaFilePath='/Users/peiyuwu/Development/pyDev/py3_8_16/MLOPS/DE_PostgresDB/file/STAllDataSchema.csv',
        columnList=[
            'dt', 'memo', 'commondata1', 'commondata2', 'commondata3', 'commondata4', 'commondata5',
            'commondata6', 'commondata7', 'commondata8', 'commondata9', 'commondata10', 'uniquechar1',
            'uniquechar2', 'uniquechar3', 'uniquechar4', 'uniquechar5', 'uniquechar6', 'uniquechar7',
            'uniquechar8', 'uniquechar9', 'uniquechar10', 'uniqueint1', 'uniqueint2', 'uniqueint3',
            'uniqueint4', 'uniqueint5', 'uniqueint6', 'uniqueint7', 'uniqueint8', 'uniqueint9',
            'uniqueint10', 'uniquefloat1', 'uniquefloat2', 'uniquefloat3', 'uniquefloat4', 'uniquefloat5',
            'uniquefloat6', 'uniquefloat7', 'uniquefloat8', 'uniquefloat9', 'uniquefloat10', 'uniquefloat11',
            'uniquefloat12', 'uniquefloat13', 'uniquefloat14', 'uniquefloat15', 'uniquestring1',
            'uniquestring2', 'uniquestring3', 'uniquestring4', 'uniquestring5', 'uniquejason'
        ]
    )
    print(dfColumnNameMemoDict)
