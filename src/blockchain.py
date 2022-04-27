__version__ = "1.0.0"
__author__ = "Zac Foteff"

import hashlib
import json
import time
from src.block import Block
from bin.logger import Logger


logger = Logger("blockchain")


class Blockchain:
    """
    Blockchain class object"""

    def __init__(
        self, create_time: float = time.time(), modify_time: float = time.time()
    ) -> None:
        self.__chain = []
        self.__create_time = create_time
        self.__modify_time = modify_time

    @property
    def size(self) -> int:
        return len(self.chain)

    def __persist(self) -> bool:
        pass

    def __restore(self) -> bool:
        pass

    def hash_block(self, block: Block) -> str:
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
        pass
