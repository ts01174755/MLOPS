import pandas as pd
import time


class ClearCourseUrl():
    def __init__(self):
        pass

    def clear_course_url(self, MONGODB, POSTGRESDB, queryFilter, PROGRESDB_SCHEMA_DICT):
        # 取得資料
        response = MONGODB.find_document(
            collection_name='course_collection',
            query=queryFilter
        )

        responses_df = pd.DataFrame(
            response[0]['data'],
            columns=['uniquechar2', 'uniquechar3', 'uniquechar4', 'uniquestring1']
        )

        responses_df["dt"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        responses_df["memo"] = PROGRESDB_SCHEMA_DICT["memo"]
        responses_df["commondata1"] = '課程規劃'
        responses_df['uniquechar1'] = responses_df.index + 1
        responses_df = responses_df[['dt', 'memo', 'commondata1', 'uniquechar1', 'uniquechar2', 'uniquechar3', 'uniquechar4', 'uniquestring1']]

        print(responses_df)

        # 連接儲存解析後的DataBase
        conn = POSTGRESDB.connectSQLAlchemy()
        responses_df.to_sql(
            'course_url',
            conn,
            schema='original',
            if_exists="replace",
            index=False
        )

if __name__ == '__main__':
    pass