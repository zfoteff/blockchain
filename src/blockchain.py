__version__ = "1.0.0"
__author__ = "Zac Foteff"

import hashlib
import json
import time

from resources.constants import *
from resources.logger import Logger

from src.block import Block

log = Logger("blockchain")


class Blockchain:
    """
    Blockchain class object"""

    def __init__(
        self,
        name: str = DEFAULT_CHAIN_NAME,
        owner: str = DEFAULT_CHAIN_OWNER,
        chain: list = None,
        create_time: float = time.time(),
        modify_time: float = time.time(),
    ) -> None:
        self.__name = name
        self.__owner = owner
        self.__chain = chain
        self.__create_time = create_time
        self.__modify_time = modify_time
        self.__pending_transactions = list()

        if self.__chain is None:
            self.__chain = list()
            self.__chain.append(Block(0, 0, {}, self.get_current_hash()))

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
            block.hash_value = self.hash_block(block)
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
            return self.get_last_block().hash_value

    def prove_work(self) -> int:
        """Solve an algorithm and get a new proof for a block

        Returns:
            int: _description_
        """
        proof = 1
        prev_proof = self.get_last_block().hash_value
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
        return f"{self.__name} (Owner: {self.__owner}) {[str(block) for block in self.__chain]}"

    def __len__(self) -> int:
        return len(self.__chain)
