from package.controller.LINECtrl import LineNotify
class LineNotifyServer():

    def __init__(self):
        pass

    def searchPostgres(self, postgresCtrl, query):
        # 連接儲存解析後的DataBase
        postgresCtrl.connect()

        # 撈取資料
        rows = postgresCtrl.query(query)
        postgresCtrl.close()

        return rows

    def postLineNotify(self, token, message):
        # 取得 token

        lineNotify = LineNotify(token)
        lineNotify.send(message)

        return 'success'

if __name__ == '__main__':
    pass