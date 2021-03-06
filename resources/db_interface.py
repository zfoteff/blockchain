__version__ = "1.0.0"
__author__ = "Zac Foteff"

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from resources.constants import *
from resources.logger import Logger
from src.blockchain import Blockchain

log = Logger("db")


class BlockchainDBInterface:
    """
    Interface for MongoDB interactions with the Block Chain
    """

    def __init__(
        self,
        db_name: str = DEFAULT_DATABASE_NAME,
        host: str = DEV_MONGO_HOST,
        port: int = DEV_MONGO_PORT,
        connection_uri: str = None,
    ) -> None:
        """Database interface script. Accepts a connection string or host ip and port to create
        an interface between blockchain objects and the MongoDB cloud host

        Args:
            db_name (str, optional): Name of the database to create a connection with. Defaults
            to DEFAULT_DATABASE_NAME.
            host (str, optional): Database host. Defaults to DEV_MONGO_HOST.
            port (int, optional): Database port on host. Defaults to DEV_MONGO_PORT.
            connection_uri (str, optional): Optional connection URI. Will apply this value if
            provided, otherwise, it will default to attempting to connect through host and port.
            Defaults to None.
        """
        self.__db_name = db_name
        self.__host = host
        self.__port = port
        self.__connection_uri = connection_uri
        self.__db_client = None

        self.__db_client = (
            MongoClient(host=connection_uri)
            if connection_uri is not None
            else MongoClient(host=host, port=port)
        )

        self.__db_client = self.__db_client.get_database(self.__db_name)

    @property
    def db_name(self) -> str:
        return self.__db_name

    def connect(self) -> bool:
        """Open a connection to the database"""
        try:
            self.__db_client = (
                MongoClient(host=self.__connection_uri)
                if self.__connection_uri is not None
                else MongoClient(host=self.__host, port=self.__port)
            )
            log("[+] Successfully connected to the database")
            return True
        except ConnectionFailure as e:
            log(f"[-] Failed to open a connection to the database: {e}", "e")
            return False

    def disconnect(self) -> None:
        """Close the connection to the database"""
        self.__db_client.close()
        log("[X] Sucessfully closed connection to database")

    def persist_chain(self, chain: Blockchain) -> None:
        """_summary_

        Args:
            chain (Blockchain): Chain that should be persisted to the database.
            New chains will create a new collection in the DB. The data for existing
            chains will be updated from the pending transactions.
        """

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

    @staticmethod
    def restore_chain(self, chain: Blockchain) -> None:
        """_summary_

        Args:
            chain (Blockchain): Chain that should be restored from the database. Chains that
            do not exist will throw an error
        """
        pass
