__version__ = "1.0.0"
__author__ = "Zac Foteff"

import hashlib
import json
import time

from bin.constants import *
from bin.db_helper import MongoDBHelper
from bin.logger import Logger

from src.block import Block

logger = Logger("blockchain")


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

        self.__db_helper = MongoDBHelper(db_collection=self.__name)

        genesis_block = Block(value={"purpose": "Genesis Block"})
        append_result = self.append_block(genesis_block)

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

    def __persist(self) -> bool:
        """Persist a blockchain instance to the database

        Returns:
            bool: Return true if the object is persisted to the database, false otherwise
        """
        pass

    def __restore(self) -> bool:
        """Restore blockchain object from the database

        Returns:
            bool: Return true if object is restored from the database, false otherwise
        """
        pass

    def append_block(self, block: Block) -> bool:
        """Append a block to the chain. Should also hash the object and set the previous hash value

        Args:
            block (Block): Defaults to None.
        Returns:
            bool: _description_
        """
        if block is not None:
            block.prev_hash = self.get_current_hash()
            encoded_block = str(block.to_dict()).encode()
            hash = hashlib.sha256(encoded_block).hexdigest()
            block.hash = hash
            self.__chain.append(block)
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

    def proof_of_work(self) -> dict:
        pass

    def to_dict(self) -> dict:
        return {
            "name": self.__name,
            "owner": self.__owner,
            "chain": self.__chain,
            "pending_transactions": self.__pending_transactions,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time,
        }

    def metadata(self) -> dict:
        return {
            "name": self.__name,
            "owner": self.__owner,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time,
        }

    def __str__(self) -> str:
        return f"{self.__name} (Owner: {self.__owner}) {self.__chain}"

    def __len__(self) -> int:
        return len(self.__chain)
