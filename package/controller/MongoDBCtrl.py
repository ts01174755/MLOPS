from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError

class MongoDBCtrl:
    def __init__(self, user_name, user_password, host, port, database_name):
        print(f"mongodb://{user_name}:{user_password}@{host}:{port}/{database_name}?authSource=admin&retryWrites=true&w=majority")
        self.client = MongoClient(f"mongodb://{user_name}:{user_password}@{host}:{port}/{database_name}?authSource=admin&retryWrites=true&w=majority")
        self.database = self.client[database_name]

    def insert_document(self, collection_name, document): # 新增資料
        collection = self.database[collection_name]
        try:
            document_id = collection.insert_one(document).inserted_id
            return {'success': True, 'message': 'Document inserted successfully', 'document_id': str(document_id)}
        except DuplicateKeyError as e:
            return {'success': False, 'message': str(e)}
        except PyMongoError as e:
            return {'success': False, 'message': str(e)}

    def find_document(self, collection_name, query, projection=None, limit=None, sort=None): # 查詢資料
        collection = self.database[collection_name]
        if limit is None:
            results = collection.find(query, projection=projection, sort=sort)
        else:
            results = collection.find(query, projection=projection, limit=limit, sort=sort)
        return [result for result in results]

    def find_one_document(self, collection_name, query, projection=None): # 查詢資料
        collection = self.database[collection_name]
        result = collection.find_one(query, projection=projection)
        return result

    def update_document(self, collection_name, query, update):  # 更新資料
        collection = self.database[collection_name]
        result = collection.update_many(query, update)
        return {'success': True, 'message': 'Documents updated successfully', 'modified_count': result.modified_count}

    def delete_document(self, collection_name, query): # 刪除資料
        collection = self.database[collection_name]
        result = collection.delete_many(query)
        return {'success': True, 'message': 'Documents deleted successfully', 'deleted_count': result.deleted_count}

    def count_documents(self, collection_name, query): # 計算資料筆數
        collection = self.database[collection_name]
        count = collection.count_documents(query)
        return count

    def create_index(self, collection_name, key_or_list, unique=False): # 建立索引
        collection = self.database[collection_name]
        index_name = collection.create_index(key_or_list, unique=unique)
        return index_name

    def list_indexes(self, collection_name): # 列出索引
        collection = self.database[collection_name]
        indexes = collection.index_information()
        return indexes

    def drop_index(self, collection_name, index_name): # 刪除索引
        collection = self.database[collection_name]
        collection.drop_index(index_name)
        return {'success': True, 'message': 'Index dropped successfully'}

    def create_collection(self, collection_name): # 建立資料表
        collection = self.database.create_collection(collection_name)
        return {'success': True, 'message': 'Collection created successfully'}

    def list_collections(self): # 列出資料表
        collections = self.database.list_collection_names()
        return collections

    def drop_collection(self, collection_name): # 刪除資料表
        collection = self.database[collection_name]
        collection.drop()
        return {'success': True, 'message': 'Collection dropped successfully'}

    def aggregate(self, collection_name, pipeline): # 聚合資料
        collection = self.database[collection_name]
        results = collection.aggregate(pipeline)
        return [result for result in results]
