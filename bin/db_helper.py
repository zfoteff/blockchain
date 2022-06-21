__version__ = "1.0.0"
__author__ = "Zac Foteff"

from pymongo import MongoClient

from bin.constants import *
from bin.logger import Logger

log = Logger("db")


class BlockchainDBController:
    """
    Helper class for MongoDB interactions
    """
    def __init__(
        self,
        db_name: str = DEFAULT_DATABASE_NAME,
        db_collection: str = DEFAULT_CHAIN_NAME,
    ) -> None:
        self.__db_name = db_name
        self.__db_collection_name = db_collection
        self.__db_client = MongoClient(host=DEV_MONGO_HOST, port=DEV_MONGO_PORT)
        self.__db = self.__db_client.get_database(self.__db_name)
        self.__db_collection = self.__db.get_collection(self.__db_collection_name)

    @property
    def db_name(self) -> str:
        return self.__db_name

    @property
    def db(self):
        return self.__db

    @property
    def db_collection_name(self) -> str:
        return self.__db_collection_name

    @property
    def collection(self):
        return self.__db_collection

    def get_database(self):
        client = MongoClient(host=DEV_MONGO_HOST, port=int(DEV_MONGO_PORT))
        db = client[self.__db_name]
        log(f"[+] Connected to ")
        return db

    def get_client(self):
        pass
