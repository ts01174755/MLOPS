import os; import sys;
os.chdir(sys.argv[1])
sys.path.append(os.getcwd())
from package.CICD.MLFlow import MLFlow
from package.controller.MongoDBCtrl import MongoDBCtrl
from dotenv import load_dotenv, find_dotenv



if __name__ == '__main__':
    print('Here is MongoDB')

    # 連接MongoDB
    load_dotenv(find_dotenv('env/.env'))
    mongodb = MLFlow(MongoDBCtrl(
        user_name=os.getenv('MongoDB_USER'),
        user_password=os.getenv('MongoDB_PASSWORD'),
        host=os.getenv('MongoDB_HOST'),
        port=int(os.getenv('MongoDB_PORT')),
        database_name='originaldb'
    ))
    COLLECTION = sys.argv[2]

    # 刪除collection - 等價於刪除table
    # print(mongodb.drop_collection(COLLECTION))

    # 新增collection - 等價於建立table
    print(mongodb.create_collection(COLLECTION))

    # # 新增collection - 等價於建立table
    # print(mongodb.create_collection('test'))
    #
    # # 新增document - 等價於建立row
    # print(mongodb.insert_document('test', {'name': 'Peter', 'age': 18}))
    #
    # # 查詢document - 等價於查詢row
    # print(mongodb.find_one_document('test', {'name': 'Peter'}))
    #
    # # 更新document - 等價於更新row
    # print(mongodb.update_document('test', {'name': 'Peter'}, {'$set': {'age': 19}}))
    #
    # # 刪除document - 等價於刪除row
    # print(mongodb.delete_document('test', {'name': 'Peter'}))
    #
    # # 刪除collection - 等價於刪除table
    # print(mongodb.drop_collection('test'))
