import time


class Block:
    """Block class object. Contains a block's value, proof, hash, and previous hash value. If 
    the object does not have a hash, then the object should be considered an unsaved element. 
    The block's value should be represented by the 

    TODO: Check the object's hash before setting the dirty flag
    """
    def __init__(
        self,
        index: int = 0,
        value: dict = None,
        proof: float = 0,
        prev_hash: str = None,
        dirty: bool = True,
        create_time: float = time.time(),
        modify_time: float = time.time(),
    ) -> None:
        self.__index = index
        self.__value = value
        self.__proof = proof
        self.__prev_hash = prev_hash
        self.__dirty = dirty
        self.__create_time = create_time
        self.__modify_time = modify_time

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
    def proof(self) -> int:
        return self.__proof

    @property
    def prev_hash(self) -> str:
        return self.__prev_hash

    @prev_hash.setter
    def prev_hash(self, prev_hash) -> None:
        self.__prev_hash = prev_hash

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @dirty.setter
    def dirty(self, dirty) -> None:
        self.__dirty = dirty

    @property
    def create_time(self) -> int:
        return self.__create_time

    @property
    def modify_time(self) -> int:
        return self.__modify_time

    @modify_time.setter
    def modify_time(self, modify_time) -> None:
        self.__modify_time = modify_time

    def metadata(self) -> dict:
        """Return metadata of block object

        Returns:
            dict: JSON object containing block metadata
        """
        return {
            "index": self.__index,
            "proof": self.__proof,
            "prev_hash": self.__prev_hash,
        }

    def to_dict(self) -> dict:
        """Return a dictionary representation of this block object. Should be used instead of the 
        built in __to_dict__() function for database insertions

        Returns:
            dict: JSON representation of the 
        """
        return {
            "index": self.__index,
            "value": self.__value,
            "proof": self.__proof,
            "prev_hash": self.__prev_hash,
            "dirty": self.__dirty,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time,
        }
