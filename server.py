__version__ = "1.1.1"
__author__ = "Zac Foteff"

import time
import sys

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse

from resources.constants import *
from resources.logger import Logger
from resources.db_interface import BlockchainDBInterface
from src.models import BlockChainModel, BlockModel
from src.block import Block
from src.blockchain import Blockchain


log = Logger("api")
cache = dict()  # [Chain name, Chain obj.]
db_interface = BlockchainDBInterface(host="0.0.0.0", port=27017)

app = FastAPI(
    title="Blockchain Demo",
    description="Blockchain demo application",
    version=__version__,
)
app_start_time = time.time()


def pull_chain(chain_name: str) -> Blockchain | None:
    """Retrieve a chain from storage. Checks if the chain exists in the cache, then attempts
    to retreive the chain from the database. Returns the found chain, or None

    Args:
        chain_name (str): Name of the chain to retrieve from storage
    Returns:
        Blockchain | None: Found blockchain. Returns the chain if one is found, returns
        none if no chain is found with that id
    """
    #   Check if the chain exists in the cache
    for chain in cache:
        if chain[chain_name] == chain_name:
            log("[+] Restored chain from the cache", "d")
            return chain["chain_obj"]

    #   TODO Check if the chain can be restored from storage
    retreived_chain = None
    if db_interface.restore_chain(chain_name):
        return retreived_chain

    #   TODO Cache the chain if it is restored from storage

    #   If the chain cannot be retrieved from the cache return None
    return None


def cache_chain(chain: Blockchain) -> bool:
    """Adds a chain to the cache. The cache should be limited to 25 chains.
    If a new chain is pushed to a full cache, the oldest chain should be removed from the cache.
    The chain's modified_date should be the bases for the age of the chain in the cache. The
    chain should not be added to the cache if an instance already exists there

    Args:
        chain (Blockchain): Chain that should be added to the cache
    Returns:
        bool: _description_
    """
    if pull_chain(chain.name) is not None:
        #   If the chain already exists in the cache -> exit the function
        log("[*] The chain already exists in the cache . . .", "w")
        return False

    #   Remove oldest chain from the cache if there are more than 25 chains in the cache
    if len(cache) >= 25:
        oldest = ("none", None)
        for chain_name, chain_obj in cache:
            if chain_obj.modified_date < oldest[1] or oldest[1] == None:
                oldest = (chain_name, chain_obj.modified_time)

    else:
        cache[chain.name] = chain
        log(f"[-+-] Added chain {str(chain)} to the cache")

    return True


@app.on_event("startup")
async def startup():
    if db_interface.connect():
        log(f"[-+-] Started listening for events at: http://127.0.0.1:8000")
    else:
        log(f"[-X-] Failed to connect to the database. Shutting down . . .")
        sys.exit(1)


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event handler. Should:
    * Disconnect from the database
    * Persist all dirty chains
    * Clear the cache
    * Disconnect from the database
    """
    cache = None
    log(f"[-X-] Cleared cache")
    db_interface.disconnect()
    log(f"[-X-] Shutdown blockchain application")
    sys.exit(0)


@app.get("/", status_code=200, include_in_schema=False)
async def index() -> JSONResponse:
    """Root endpoint for blockchain interactions

    Returns:
        dict: JSON reponse that can be viewed in the browers, or postman, to
        confirm that the application is running
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "response": "Thanks for navigating to the root endpoint of my blockchain api!",
            "timestamp": time.time(),
        },
    )


@app.get("/favicon.ico", status_code=200, include_in_schema=False)
async def favicon() -> FileResponse:
    """Return favicon for the application page

    Returns:
        FileResponse: Favicon image
    """
    return FileResponse("static/favicon.ico")


@app.get("/info/", status_code=200, tags=["Monitoring"])
async def info_digest() -> JSONResponse:
    """Return a digest of information about the health of the server + the current state of
    the blockchain

    Returns:
        JSONResponse: Information digest of the health of the server
    """
    uptime = time.time() - app_start_time

    return JSONResponse(
        status_code=200,
        content={
            "status": "Running",
            "uptime": uptime,
            "cache": [chain.metadata() for chain in cache.values()],
        },
    )


@app.get("/info/health/", status_code=200, tags=["Monitoring"])
async def health() -> JSONResponse:
    """Return a summary of the application health. Should ping services like the database
    and other microservices involved in the application
    TODO Finish description
    TODO Create and return health response

    Returns:
        JSONResponse: _description_
    """
    pass


@app.get("/v1/chain/", status_code=200, tags=["Chain Methods"])
async def get_chain(
    chain_name: str = Query(
        title="Chain Name",
        alias="chain_name",
        example="zchain"
    )
) -> JSONResponse:
    """Retrieve a chain. First check if the chain exists in the cache. If it does not, then
    retrieve it from the database and add it too the cache. Should return the serialized chain

    Args:
        chain_name (str): Name of the chain the request is seeking to find

    Returns:
        JSONResponse: JSON representation of the chain
    """
    # TODO Retrieve chain from cache / database
    # TODO Add chain to cache if necessary

    chain = pull_chain(chain_name=chain_name)

    if chain is None:
        #   TODO Chain is not in database -> restore from db
        pass

    return JSONResponse(status_code=200, content={"Chain name": chain_name})


@app.post("/v1/chain/", status_code=201, tags=["Chain Methods"])
async def register_chain(req_chain: BlockChainModel) -> JSONResponse:
    """Register chain to the applications cache of chains the applications stores
    TODO complete the chain object so that it can return the proper data on request
    TODO Add the chain to the cache

    Args:
        req (Request): Request containing the chain information.
        the body should contain
        - The chain name
        - The chain owner
    Returns:
        JSONResponse: Return a status object to the user indicating the new status of the
        chain
    """

    chain = pull_chain(req_chain["name"])

    if chain is not None:
        return JSONResponse(
            status_code=400,
            content={"result": "Failed", "reason": "Chain is already registered "},
        )

    chain = Blockchain(name=req_chain["name"], owner=req_chain["owner"])
    cache_chain(chain)

    # TODO Persist the new chain to the database

    return JSONResponse(
        status_code=201, content={"result": "Success", "chain": str(chain)}
    )


@app.get("/v1/block/{hash_value}", tags=["Block Methods"])
async def get_block(
    hash_value: str,
    parent_chain: str = Query(
        default="null",
        title="Parent chain",
        alias="parent_chain",
        example="zchain",
    ),
    proof: str = Query(default=0.0, title="Proof", alias="proof", example=1.0234),
) -> JSONResponse:
    """Return a block from a requested chain

    Args:
        req (Request): HTTP request containing the requested block's information
        The body should contain
        - The chain to query for a block
        - The hash of the requested block
    Returns:
        JSONResponse: _description_
    """

    # TODO Check if the chain is in the cache
    #   If not, retrieve the chain and add it to the cache
    # TODO Return a single block from requested chain

    if parent_chain not in cache:
        #   TODO Check if the chain can be retrieved from the database, if it can't return error
        return JSONResponse(
            status_code=400,
            content={"result": "ERROR", "reason": "Parent chain does not exist"},
        )

    chain = cache[parent_chain]
    # TODO Error if the chain does not exist in the cache or the database
    # TODO Retreive the chain from the database if it does not exist

    for block in chain.chain:
        if block.hash == hash_value and block.proof == float(proof):
            return JSONResponse(
                status_code=200,
                content={"result": "SUCCESS", "block": str(block)},
            )

    return JSONResponse(
        status_code=404,
        content={"result": "FAILURE", "reason": "Block not found in parent chain"},
    )


@app.post("/v1/block/", status_code=201, tags=["Block Methods"])
async def create_block(block: (BlockModel | None) = None) -> JSONResponse:
    """Create a new block in a selected chain

    Args:
        req (Request): HTTP request containing the new block's information.
        The body should contain
        - Chain to add the block to
        - Block value
        - Block proof
    Returns:
        JSONResponse: Status of block insertion into the chain. 201 if block is created,
        406 if the object cannot be created

    TODO Persist block to the chain
    """

    #   Validate the request body
    if block is None:
        #   If no body is submitted, return error response
        log("Empty body", "d")
        return JSONResponse(
            status_code=400,
            content={"result": "Failure", "reason": "Empty request body"},
        )

    chain_name = block["parent_chain"]
    chain = pull_chain(chain_name)

    if chain is None:
        #   If chain isnt in the cache, instantiate a new object and cache it for future use
        #   TODO Restore the chain from the database
        chain = Blockchain(name=chain_name)
        cache[chain_name] = chain

    new_block = Block(
        index=chain.next_index,
        value=block["block_value"],
        proof=block["block_proof"],
    )

    chain.append_block(new_block)
    log(f"[+] Inserted {new_block} into chain {chain}", "d")
    return JSONResponse(
        status_code=201, content={"result": "Success", "created": str(new_block)}
    )


if __name__ == "__main__":
    from uvicorn import run

    run(app="server:app", log_level="debug", reload=True)
