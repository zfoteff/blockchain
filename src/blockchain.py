__version__ = "1.0.0"
__author__ = "Zac Foteff"

import hashlib
import json
import time
from src.block import Block
from bin.logger import Logger
from bin.constants import *


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

    def hash_block(self, block: Block=None) -> str:
        pass

    def append_block(self, block: Block = None) -> bool:
        pass

    def get_last_block(self) -> dict:
        """Retrieve the last inserted block in the chain

        Returns:
            dict: JSON representation of the block's data
        """
        return self.chain[-1]

    def proof_of_work(self) -> dict:
        pass

    def to_dict(self) -> dict:
        pass

    def metadata(self) -> dict:
        pass

    def __str__(self) -> str:
        return f"{self.__name} (Owner: {self.__owner}) {self.__chain}"

    def __len__(self) -> int:
        return len(self.__chain)
