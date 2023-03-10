import os; import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
import uvicorn


if __name__ == '__main__':
    print('Here is 1_projectExampleTest.py')

    app = FastAPI()
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: str = None):
        return {"item_id": item_id, "q": q}

    uvicorn.run(app, host="127.0.0.1", port=8000)
    # # 連接MongoDB
    # load_dotenv(find_dotenv('env/.env'))
    # mongodb = MLFlow(MongoDBCtrl(
    #     user_name=os.getenv('MongoDB_USER'),
    #     user_password=os.getenv('MongoDB_PASSWORD'),
    #     host=os.getenv('MongoDB_HOST'),
    #     port=int(os.getenv('MongoDB_PORT')),
    #     database_name='originaldb'
    # ))
    #
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
    # # 查詢document - 等價於查詢row
    # print(mongodb.find_one_document('test', {'name': 'Peter'}))
    #
    # # 刪除document - 等價於刪除row
    # print(mongodb.delete_document('test', {'name': 'Peter'}))
    #
    # # 刪除collection - 等價於刪除table
    # print(mongodb.drop_collection('test'))
