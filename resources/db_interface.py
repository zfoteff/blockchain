__version__ = "1.0.0"
__author__ = "Zac Foteff"

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from resources.constants import *
from resources.logger import Logger
from src.blockchain import Blockchain

log = Logger("db_interface")


class BlockchainDBInterface:
    """Interface for MongoDB interactions with the Block Chain"""

    def __init__(
        self,
        db_name: str = DEFAULT_DATABASE_NAME,
        connection_uri: str = MONGO_URL,
    ) -> None:
        """Database interface script. Accepts a connection string or host ip and port to create
        an interface between blockchain objects and the MongoDB cloud host

        Args:
            db_name (str, optional): Name of the database to create a connection with. Defaults
            to DEFAULT_DATABASE_NAME.
            connection_uri (str): Connection URI. Will apply this value if provided, otherwise,
            it will default to attempting to connect through host and port.
        """
        self.__db_name = db_name
        self.__connection_uri = connection_uri

        #   These variables are set after
        self.__db_client = None
        self.__db = None

    @property
    def db_name(self) -> str:
        """Database name"""
        return self.__db_name

    def connect(self) -> bool:
        """Open a connection to the database

        Returns:
            bool: Return true if connection is successful
        """
        try:
            self.__db_client = (
                MongoClient(host=self.__connection_uri)
                if self.__connection_uri is not None
                else MongoClient(host=self.__host, port=self.__port)
            )
            self.__db = self.__db_client.get_database(self.__db_name)
            log("[-+-] Successfully connected to the database")
            return True
        except ConnectionFailure as e:
            log(f"[-X-] Failed to open a connection to the database: {e}", "e")
            return False

    def disconnect(self) -> None:
        """Close the connection to the database"""
        self.__db_client.close()
        log("[-X-] Sucessfully closed connection to database")

    def persist_chain(self, chain: Blockchain) -> None:
        """Persist a chain to the database

        Args:
            chain (Blockchain): Chain that should be persisted to the database.
            New chains will create a new collection in the DB. Existing
            chains will be updated from the pending transactions.
        """
        
        log(f"[*] Persisting chain {chain.name} to the database")
        collection = self.__db_client.get_collection(chain.name)

        if collection is None:
            #   If collection does not exist in the DB, create the collection
            log(
                f"[-] Cannot find collection for chain {chain.name}. Creating . . .",
                "w",
            )
            collection = self.__db_client.create_collection(chain.name)
        else:
            log(f"[*] Found collection for chain {chain.name}", "d")

        # TODO Should ensure validity of chain before persisting blocks
        #    if !chain.is_valid():
        #       log(error)

        for block in chain.chain:
            # NOTE Currently iterates through entire chain to find dirty blocks (inefficient)
            # TODO Refactor to persist from a given chain's pending transactions
            if block.dirty:
                log(
                    f"\n[+] Persisted block {str(block)} to the {chain.name} collection",
                    "d",
                )
                collection.insert_one(block.to_dict())
                block.dirty = False

        log(f"[+] Persisted chain {chain.name}")

    def restore_chain(self, chain_name: str) -> Blockchain | None:
        """Restore a chain from the database using the name of the chain

        Args:
            chain_name (str): Chain that should be restored from the database. Chains that
            do not exist will throw an error
        Returns:
            bool: True if chain is successfully restored, false otherwise
        """
        collection = self.__db.get_collection(name=chain_name)
        log(collection)
        if collection is None:
            log(f"[-] No collection found for chain f{chain_name}")
            return collection

        result = collection.find_one(filter={"chain_name": chain_name})
        log(result)

        return None
