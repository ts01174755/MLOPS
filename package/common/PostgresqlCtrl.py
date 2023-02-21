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
        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

class DatabaseProxy:
    def __init__(self, host, database, user, password):
        self.db = Database(host, database, user, password)

    def execute(self, query):
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows

    def close(self):
        self.db.close()

# 測試程式碼
db_proxy = DatabaseProxy("your_host", "your_database", "your_username", "your_password")
result = db_proxy.execute("SELECT * FROM your_table")
print(result)
db_proxy.close()