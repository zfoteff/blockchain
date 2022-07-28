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
    owner: str | None
    create_time: float | None
    modify_time: float | None

class BlockRequestModel(BaseModel):
    chain_name: str 
    hash_value: str
    proof: float