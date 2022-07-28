__version__ = "1.1.0"
__author__ = "Zac Foteff"

import time
import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from uvicorn import run

from resources.constants import *
from resources.logger import Logger
from resources.db_interface import BlockchainDBInterface
from src.block import Block
from src.blockchain import Blockchain

app = FastAPI(title="Blockchain Demo")

log = Logger("api")
cache = dict()  # [Chain name, Chain obj.]
db_interface = BlockchainDBInterface()

app_start_time = time.time()


@staticmethod
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


@app.on_event("startup")
async def startup():
    if db_interface.connect():
        log(f"[-+-] Started listening for events at: http://127.0.0.1:8080")
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


@app.get(path="/favicon.ico", status_code=200, include_in_schema=False)
async def favicon() -> FileResponse:
    """Return favicon for the application page

    Returns:
        FileResponse: Favicon image
    """
    return FileResponse("static/favicon.ico")


@app.get(path="/", status_code=200)
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


@app.get(path="/info/", status_code=200)
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
    
    
@app.get(path="/info/health", status_code=200)
async def health() -> JSONResponse:
    """Return a summary of the application health. Should ping services like the database 
    and other microservices involved in the application
    TODO Finish description
    TODO Create and return health response

    Returns:
        JSONResponse: _description_
    """
    pass


@app.get(path="/v1/chain/", status_code=200)
async def get_chain(req: Request) -> JSONResponse:
    """Retrieve a chain. First check if the chain exists in the cache. If it does not, then
    retrieve it from the database and add it too the cache. Return the serialized chain

    Args:
        req (Request): Request containing infomation about the requested chain. The
        body should contain
        - The chain name
        - The chain owner (optional)
    Returns:
        JSONResponse: Serialized chain
    """
    # TODO Validate body
    return JSONResponse(status_code=501, content={})


@app.post(path="/v1/register_chain/", status_code=201)
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


@app.post(path="/v1/block/", status_code=201)
async def get_block(req: Request) -> JSONResponse:
    """Return a block from a requested chain

    Args:
        req (Request): HTTP request containing the requested block's information
        The body should contain
        - The chain to query for a block
        - The hash of the requested block
    Returns:
        JSONResponse: _description_
    """

    # TODO Return a single block from requested chain
    
    pass


@app.post(path="/v1/block/", status_code=201)
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
    run(app)
