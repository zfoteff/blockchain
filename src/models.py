from pydantic import BaseModel


class BlockModel(BaseModel):
    parent_chain: str
    proof: float
    value: dict
    hash_value: str
    prev_hash: str
    create_time: float
    modify_time: float


class BlockChainModel(BaseModel):
    name: str
    owner: str