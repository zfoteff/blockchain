__version__ = "1.1.0"
__author__ = "Zac Foteff"

import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from docs.constants import *
from docs.logger import Logger
from src.block import Block
from src.blockchain import Blockchain

app = FastAPI(title="Blockchain Demo")
log = Logger("api")
cache = dict()
app_start_time = time.time()
log(f"[-+-] Started listening for events at {app.host}")


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


@app.get(path="/v1/info/", status_code=200)
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


@app.get(path="/v1/chain/", status_code=200)
async def get_chain(req: Request) -> JSONResponse:
    """_summary_

    Args:
        req (Request): _description_
    Returns:
        JSONResponse: _description_
    """
    return JSONResponse(status_code=501)


@app.post(path="/v1/register_chain/", status_code=201)
async def register_chain(req: Request) -> JSONResponse:
    """Register chain to the applications cache of chains the applications stores
    TODO: complete the chain object so that it can return the proper data on request

    Args:
        req (Request): Request containing the chain information.
        the body should contain
        - The chain name
        - Teh chain owner
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
        #   If body parameters do not include 
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
    log(f"[+] Inserted {block} into chain {chain}")
    return JSONResponse(
        status_code=201, content={"result": "Success", "created": str(block)}
    )