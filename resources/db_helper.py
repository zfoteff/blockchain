__version__ = "1.0.0"
__author__ = "Zac Foteff"

from pymongo import MongoClient

from resources.constants import *
from resources.logger import Logger

log = Logger("db")


class BlockchainDBController:
    """
    Helper class for MongoDB interactions with the Block Chain
    """

    def __init__(
        self,
        db_name: str = DEFAULT_DATABASE_NAME,
        db_collection: str = DEFAULT_CHAIN_NAME,
        host: str = DEV_MONGO_HOST,
        port: int = DEV_MONGO_PORT,
        connection_uri: str = None,
    ) -> None:
        """Database interface script. Accepts a connection string or host ip and port to create
        an interface between blockchain objects and the MongoDB cloud host

        Args:
            db_name (str, optional): Name of the database to create a connection with. Defaults
            to DEFAULT_DATABASE_NAME.
            db_collection (str, optional): Collection to access in the database. The collection
            name should correspond with the name of the chain being stored there. Defaults to
            DEFAULT_CHAIN_NAME.
            host (str, optional): _description_. Defaults to DEV_MONGO_HOST.
            port (int, optional): _description_. Defaults to DEV_MONGO_PORT.
            connection_uri (str, optional): _description_. Defaults to None.
        """

        if connection_uri is not None:
            self.__db_client = MongoClient(host=connection_uri)
        else:
            self.__db_client = MongoClient(host=host, port=port)

        self.__db_name = db_name
        self.__db_collection_name = db_collection
        self.__db = self.__db_client.get_database(self.__db_name)
        self.__db_collection = self.__db.get_collection(self.__db_collection_name)

        if self.__db_collection is None:
            #   If collection does not exist in the DB, create the collection
            log(
                f"[-] Cannot find collection {self.db_collection_name}. Creating . . .",
                "w",
            )
            self.db_collection_name = self.__db.create_collection(
                self.__db_collection_name
            )

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
