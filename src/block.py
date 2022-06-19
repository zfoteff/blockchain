__version__ = "1.0.0"
__author__ = "Zac Foteff"

import time


class Block:
    """Block class object. Contains a block's value, proof, hash, and previous hash value. If
    the object does not have a hash, then the object should be considered an unsaved element.
    The block's value should be represented by a dictionary to allow users to customize the data
    stored in the block
    """

    def __init__(
        self,
        index: int = 0,
        proof: float = 0.0,
        value=None,
        hash_value: str = None,
        prev_hash: str = None,
        create_time: float = time.time(),
        modify_time: float = time.time(),
    ) -> None:
        """Instantiate a Block object. Blocks are created with no hash value or previous hash value

        Args:
            index (int, optional): _description_. Defaults to 0.
            proof (float, optional): _description_. Defaults to 0.
            value (dict, optional): _description_. Defaults to dict().
            create_time (float, optional): _description_. Defaults to time.time().
            modify_time (float, optional): _description_. Defaults to time.time().
        """
        if value is None:
            value = dict()
        self.__index = index
        self.__proof = proof
        self.__value = value
        self.__create_time = create_time
        self.__modify_time = modify_time
        self.__hash_value = hash_value
        self.__prev_hash = prev_hash

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, index) -> None:
        if index >= 0:
            self.__index = index

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        self.__value = value

    @property
    def proof(self) -> float:
        return self.__proof

    @property
    def hash_value(self) -> str:
        return self.__hash_value

    @property
    def prev_hash(self) -> str:
        return self.__prev_hash

    @prev_hash.setter
    def prev_hash(self, prev_hash) -> None:
        self.__prev_hash = prev_hash

    @property
    def create_time(self) -> float:
        return self.__create_time

    @property
    def modify_time(self) -> float:
        return self.__modify_time

    @modify_time.setter
    def modify_time(self, modify_time: float) -> None:
        self.__modify_time = modify_time

    def metadata(self) -> dict:
        """Return metadata digest of block object

        Returns:
            dict: JSON object containing block metadata
        """
        return {
            "index": self.__index,
            "proof": self.__proof,
            "prev_hash": self.__prev_hash,
        }

    def to_dict(self) -> dict:
        """Return a dictionary digest of this block object. Should be used instead of the
        built-in __to_dict__() function for database insertions

        Returns:
            dict: JSON digest of the block object
        """
        return {
            "index": self.__index,
            "value": self.__value,
            "proof": self.__proof,
            "hash": self.__hash_value,
            "prev_hash": self.__prev_hash,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time,
        }

    def __str__(self) -> str:
        return f"Block[{self.__index}]{self.__value}"
