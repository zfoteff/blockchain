__version__ = "1.0.0"
__author__ = "Zac Foteff"

import hashlib
import json
import time

from pymongo import MongoClient

from bin.constants import *
from bin.logger import Logger

from src.block import Block

log = Logger("blockchain")


class Blockchain:
    """
    Blockchain class object"""

    def __init__(
        self,
        name: str = DEFAULT_CHAIN_NAME,
        owner: str = DEFAULT_CHAIN_OWNER,
        create_time: float = time.time(),
        modify_time: float = time.time(),
    ) -> None:
        self.__name = name
        self.__owner = owner
        self.__chain = list()
        self.__pending_transactions = list()
        self.__create_time = create_time
        self.__modify_time = modify_time
        self.__db_collection = None
        self.__db_client = MongoClient(host=DEV_MONGO_HOST, port=int(DEV_MONGO_PORT))
        self.__db = self.__db_client.get_database(DEFAULT_DATABASE_NAME)
        self.__db_collection = self.__db.get_collection(self.__name)

        if self.__db_collection is None:
            # Initialize the chains collection in the DB if it doesn't exist
            log(f"[-] No collection exists for chain {self.__name}. Creating . . .")
            self.__db_collection = self.__db.create_collection(self.__name)

        if self.__restore():
            self.__dirty = False
        else:
            genesis_block = Block(value={"purpose": "Genesis Block"})
            self.append_block(genesis_block)
            self.__dirty = True

    @property
    def name(self) -> str:
        return self.__name

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def chain(self) -> list:
        return self.__chain

    @property
    def pending_transactions(self) -> list:
        return self.__pending_transactions

    @property
    def size(self) -> int:
        """Return length of the chain"""
        return len(self.__chain)

    @property
    def create_time(self) -> float:
        return self.__create_time

    @property
    def modify_time(self) -> float:
        return self.__modify_time

    @modify_time.setter
    def modify_time(self, modify_time: float) -> None:
        self.__modify_time = modify_time

    def __persist(self) -> None:
        """Persist a blockchain instance to the database

        Returns:
            bool: Return true if the object is persisted to the database, false otherwise
        """
        if self.__db_collection.find_one({"chain_name": {"$exists": "false"}}):
            chain_update_filter = {"chain_name": self.__name}
            new_chain_value = {"$set": self.to_dict()}
            self.__db_collection.update_one(
                chain_update_filter, new_chain_value, upsert=True
            )

        for block in self.__chain:
            block_update_filter = {"hash": block.hash}
            block_values = {"$set": block.to_dict()}
            self.__db_collection.update_one(
                block_update_filter, block_values, upsert=True
            )

        log("[+] Persisted chain object to the database")

    def __restore(self) -> bool:
        """Restore blockchain object from the database

        Returns:
            bool: Return true if object is restored from the database, false otherwise
        """
        chain_metadata = self.__db_collection.find_one({"chain_name": {"$exists": "true"}})
        if chain_metadata is None:
            log("[*] No metadata found for chain. Creating new colleciton . . .", "w")
            self.__persist()
            return False

        self.__name = chain_metadata["chain_name"]
        self.__owner = chain_metadata["owner"]
        self.__create_time = chain_metadata["create_time"]
        self.__modify_time = chain_metadata["modify_time"]

        for block_data in self.__db_collection.find({"hash": {"$exists": "true"}}):
            new_block = Block(
                index=block_data["index"],
                proof=block_data["proof"],
                value=block_data["value"],
                hash=block_data["hash"],
                prev_hash=block_data["prev_hash"],
                create_time=block_data["create_time"],
                modify_time=block_data["modify_time"],
            )
            self.chain.append(new_block)
        log(f"[+] Restored chain {self.to_dict()}")
        return True

    def hash_block(self, block: Block) -> str:
        """Generate hash of a inputted block

        Args:
            block (Block): Block to hash
        Returns:
            str: Hash digest of the block contents
        """
        encoded_block = json.dumps(block.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def append_block(self, block: Block) -> bool:
        """Append a block to the chain. Should also hash the object and set the previous hash value

        Args:
            block (Block): Defaults to None.
        Returns:
            bool: _description_
        """
        if block is not None:
            block.prev_hash = self.get_current_hash()
            block.hash = self.hash_block(block)
            self.__chain.append(block)
            self.__persist()
            return True
        return False

    def get_last_block(self) -> Block | None:
        """Retrieve the last inserted block in the chain

        Returns:
            Block: Last block in the chain, or None if the chain is empty
        """
        try:
            return self.chain[-1]
        except IndexError:
            return None

    def get_current_hash(self) -> str:
        """Get the hash of the last block in the chain

        Returns:
            str: Hash of the terminal block in the chain
        """
        if self.get_last_block() is None:
            return hashlib.sha256("genesis".encode()).hexdigest()
        else:
            return self.get_last_block().hash

    def prove_work(self) -> int:
        """Solve an algorithm and get a new proof for a block

        Returns:
            int: _description_
        """
        proof = 1
        prev_proof = self.get_last_block().hash
        if prev_proof is None:
            return -1

        check_proof = False
        while check_proof:
            hash = hashlib.sha256(
                str(proof**2 - prev_proof**2).encode()
            ).hexdigest()
            if hash[:4] == "0000":
                check_proof = True

            proof += 1
        return proof

    def to_dict(self) -> dict:
        return {
            "name": self.__name,
            "owner": self.__owner,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time,
        }

    def metadata(self) -> dict:
        return {
            "name": self.__name,
            "owner": self.__owner,
        }

    def __str__(self) -> str:
        return f"{self.__name} (Owner: {self.__owner}) {self.__chain}"

    def __len__(self) -> int:
        return len(self.__chain)
