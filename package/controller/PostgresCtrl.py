import psycopg2

class PostgresCtrl:
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

    # 查詢特定Table的Schema
    def queryTableSchema(self, table):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM information_schema.columns WHERE table_name = '{table}';")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def queryTableSchemaDataFrame(self, table, columns=None):
        if columns is None:
            columns = ['table_catalog', 'table_schema', 'table_name', 'column_name', 'ordinal_position',
                       'column_default', 'is_nullable', 'data_type', 'character_maximum_length',
                       'character_octet_length', 'numeric_precision', 'numeric_precision_radix', 'numeric_scale',
                       'datetime_precision', 'interval_type', 'interval_precision', 'character_set_catalog',
                       'character_set_schema', 'character_set_name', 'collation_catalog', 'collation_schema',
                       'collation_name', 'domain_catalog', 'domain_schema', 'domain_name', 'udt_catalog', 'udt_schema',
                       'udt_name', 'scope_catalog', 'scope_schema', 'scope_name', 'maximum_cardinality',
                       'dtd_identifier', 'is_self_referencing', 'is_identity', 'identity_generation', 'identity_start',
                       'identity_increment', 'identity_maximum', 'identity_minimum', 'identity_cycle', 'is_generated',
                       'generation_expression', 'is_updatable']
        import pandas as pd
        return pd.DataFrame(self.queryTableSchema(table), columns=columns)
