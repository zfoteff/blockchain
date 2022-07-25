import string
from pydantic import BaseModel


class BlockModel(BaseModel):
    index: int
    proof: float
    value: dict
    hash_value: str
    prev_hash: str
    create_time: float
    modify_time: float


class BlockChainModel(BaseModel):
    name: str
    owner: str
    create_time: float
    modify_time: float
