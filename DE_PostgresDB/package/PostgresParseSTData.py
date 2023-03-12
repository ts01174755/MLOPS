import re


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

