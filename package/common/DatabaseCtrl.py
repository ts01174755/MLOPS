import psycopg2

class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
        return self.conn # 這裡要回傳conn, 不然會出現NoneType has no attribute 'cursor'的錯誤

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute(self, query): # 執行資料庫指令
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit() # 這裡要記得commit, 不然資料庫不會更新, 這是一個很常犯的錯誤
        cursor.close()

    def query(self, query): # 查詢資料
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows