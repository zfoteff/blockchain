__version__ = "1.0.0"
__author__ = "Zac Foteff"

from typing import Collection
from pymongo import MongoClient

from bin.logger import Logger
from bin.constants import *

log = Logger("db")

class MongoDBHelper:
    def __init__(self, db_name: str=DEFAULT_DATABASE_NAME, db_collection: str=DEFAULT_CHAIN_NAME) -> None:
        self.__db_name = db_name
        self.__db_collection_name = db_collection
        self.__db_client = MongoClient(MONGO_CONNECTION_STRING)
        self.__db = self.__db_client.get_database(self.__db_name)
        self.__db_collection = self.__db.get_collection(self.__db_collection_name)

        log(f"[-+-] Successfully connected to database {self.__db_name} and collection {self.__db_collection_name}")
        
    @property
    def db_name(self) -> str:
        return self.__db_name

    @property
    def db_collection_name(self) -> str:
        return self.__db_collection_name

    @property
    def collection(self) -> Collection:
        return self.__db_collection
