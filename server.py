__version__ = "1.1.0"
__author__ = "Zac Foteff"

from itertools import chain
import time
import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse

from resources.constants import *
from resources.logger import Logger
from resources.db_interface import BlockchainDBInterface
from src.models import BlockChainModel, BlockRequestModel, BlockModel
from src.block import Block
from src.blockchain import Blockchain


log = Logger("api")
cache = dict()  # [Chain name, Chain obj.]
db_interface = BlockchainDBInterface()

app = FastAPI(title="Blockchain Demo")
app_start_time = time.time()


def __pull_chain(chain_name: str) -> Blockchain | None:
    """Retrieve a chain from the fastApi application's cache of active

    Args:
        chain_name (str): Name of the chain to retrieve from the cache
    Returns:
        Blockchain | None: Found blockchain. Returns the chain if one is found, returns
        none if no chain is found with that id
    """
    for chain in cache:
        if chain["chain_name"] == chain_name:
            return chain["chain_obj"]

    return None

def __cache_chain(chain: Blockchain) -> bool:
    """Adds a chain to the cache. The cache should be limited to 25 chains.
    If a new chain is pushed to a full cache, the oldest chain should be removed from the cache.
    The chain's modified_date should be the bases for the age of the chain in the cache. The 
    chain should not be added to the cache if an instance already exists there

    Args:
        chain (Blockchain): Chain that should be added to the cache
    Returns:
        bool: _description_
    """
    if __pull_chain(chain.name) is not None:
        #   If the chain already exists in the cache -> exit the function
        log("[*] The chain already exists in the cache . . .", "w")
        return False


    if len(cache) >= 25:
        # TODO Add logic to remove the oldest 
        pass

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


@app.get("/favicon.ico", status_code=200, include_in_schema=False)
async def favicon() -> FileResponse:
    """Return favicon for the application page

    Returns:
        FileResponse: Favicon image
    """
    return FileResponse("static/favicon.ico")


@app.get("/", status_code=200)
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


@app.get("/info/", status_code=200)
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


@app.get("/info/health/", status_code=200)
async def health() -> JSONResponse:
    """Return a summary of the application health. Should ping services like the database
    and other microservices involved in the application
    TODO Finish description
    TODO Create and return health response

    Returns:
        JSONResponse: _description_
    """
    pass


@app.get("/v1/chain/", status_code=200)
async def get_chain(chain_name: str) -> JSONResponse:
    """Retrieve a chain. First check if the chain exists in the cache. If it does not, then
    retrieve it from the database and add it too the cache. Return the serialized chain

    Args:
        chain_name (str): Name of the chain the request is seeking to find

    Returns:
        JSONResponse: _description_
    """
    # TODO Validate query params
    # TODO Retrieve chain from cache / database
    # TODO Add chain to cache if necessary

    chain = __pull_chain(chain_name=chain_name)

    if chain is None:
        #   Chain is not in database -> restore from db
        pass

    return JSONResponse(status_code=200, content={"Chain name": chain_name})


@app.post("/v1/chain/", status_code=201)
async def register_chain(req: Request) -> JSONResponse:
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
    body = await req.json()
    chain = __pull_chain(body["chain_name"])
    if chain is not None:
        return JSONResponse(
            status_code=400,
            content={"result": "Failed", "reason": "Chain is already registered "},
        )

    chain = Blockchain(name=body["chain_name"], owner=body["chain_owner"])
    cache[chain.name] = chain
    return JSONResponse(
        status_code=201, content={"result": "Success", "chain": str(chain)}
    )


@app.get("/v1/block/")
async def get_block(chain_name: str, hash_value: str, proof: float) -> JSONResponse:
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

    return JSONResponse(status_code=200, content={"chain_name": chain_name, "hash_value": hash_value, "proof": proof})


@app.post("/v1/block/", status_code=201)
async def create_block(req: Request) -> JSONResponse:
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
    """
    body = req.json()

    #   Validate the request body
    if body is None:
        #   If no body is submitted, return error response
        return JSONResponse(
            status_code=400,
            content={"result": "Failure", "reason": "Empty request body"},
        )
    elif (
        body["chain"] is None
        or body["block_value"] is None
        or body["block_proof"] is None
    ):
        #   If body parameters are invalid
        return JSONResponse(
            status_code=400,
            content={
                "result": "Failure",
                "reason": "One or more required body values are missing",
            },
        )
    elif (
        not isinstance(body["chain"], str)
        or not isinstance(body["block_value"], dict)
        or not isinstance(body["block_proof"], float)
    ):
        return JSONResponse(
            status_code=400,
            content={"result": "Failure", "reason": "Incorrect parameter types"},
        )

    chain_name = body["chain"]
    chain = __pull_chain(chain_name)

    if chain is None:
        #   If chain isnt in the cache, instantiate a new object and cache it for future use
        chain = Blockchain(name=chain_name)
        cache[chain_name] = chain

    block = Block(
        index=chain.length + 1,
        value=body["block_value"],
        proof=body["block_proof"],
    )

    chain.append_block(block)
    log(f"[+] Inserted {block} into chain {chain}", "d")
    return JSONResponse(
        status_code=201, content={"result": "Success", "created": str(block)}
    )


if __name__ == "__main__":
    from uvicorn import run

    run(app, host="127.0.0.1", port=8080, log_level="debug")
