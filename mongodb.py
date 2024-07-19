import pymongo
import traceback
from configs.config import settings


class MongoDBProgress:
    mongo_client = None
    database_ref = None
    collection_ref = None

    def __init__(self) -> None:
        try:
            self.mongo_client = pymongo.MongoClient(f"mongodb://{settings.mongo.USER}:{settings.mongo.PASSWORD}@{settings.mongo.HOST}:{settings.mongo.PORT}/", serverSelectionTimeoutMS=settings.mongo.TIMEOUT)
        except Exception:
            print(traceback.format_exc())

    def check_database(self, database_name):
        return database_name in self.mongo_client.list_database_names()

    def check_collection_name(self, collection_name):
        return collection_name in self.database_ref.list_collection_names()

    def create_database(self, database_name):
        self.database_ref = self.mongo_client[database_name]

    def create_collection(self, database_name=None, collection_name=None):
        if self.database_ref is None:
            self.create_database(database_name=database_name)
        self.collection_ref = self.database_ref[collection_name]

    def insert_data_to_collection(self, database_name="Minio", collection_name=None, data={}):
        if self.collection_ref is None:
            self.create_collection(database_name=database_name, collection_name=collection_name)
        res = self.collection_ref.insert_one(data)
        return res.inserted_id

    def get_data(self, database_name=None, collection_name=None, query={}):
        if self.collection_ref is None:
            self.create_collection(database_name=database_name, collection_name=collection_name)
        return self.collection_ref.find_one(query) or None

    def delete_data_to_collection(self, query):
        return self.collection_ref.delete_one(query)
