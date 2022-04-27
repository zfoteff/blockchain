"""
Blockchain class object
"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

import hashlib
import json
from datetime import datetime

logger

class Blockchain:
    def __init__(self) -> None:
        self.chain = []

    @property
    def size(self) -> int:
        return len(self.chain)

    def __generate_blockchain(self):
        pass

    def __str__(self) -> str:
        pass

    def __persist(self) -> bool:
        pass

    def __restore(self) -> bool:
        pass

    def append_block(self) -> bool:
        pass

    def get_last_block(self) -> dict:
        return self.chain[-1]

    def proof_of_work(self) -> dict:
        pass

    def metadata(self) -> dict:
        pass
