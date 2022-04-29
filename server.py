__version__ = "1.0.0"
__author__ = "Zac Foteff"

import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from src.blockchain import Blockchain
from bin.constants import *
from bin.logger import Logger

app = FastAPI(title="Blockchain Demo")
log = Logger("api")
chainCache = dict()
app_start_time = time.time()
log("[-+-] Started listening for events at http://localhost:8000")


def __pull_chain(chain_name: str) -> Blockchain | None:
    """Retrieve a chain from the fastApi application's cache of active

    Args:
        chain_name (str): Name of the chain to retrieve from the cache
    Returns:
        Blockchain | None: Found blockchain. Returns the chain if one is found, returns
        none if no chain is found with that id
    """
    pass


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
    # chains = [chain.digest for chain in chainCache]


@app.get(path="/chain/", status_code=200)
async def get_chain(req: Request) -> JSONResponse:
    """_summary_

    Args:
        req (Request): _description_
    Returns:
        JSONResponse: _description_
    """
    pass

@app.post(path="/register_chain/", status_code=201)
async def register_chain(req: Request) -> JSONResponse:
    """Register a chain to the applications cache of chains the applications stores
    TODO: complete the chain object so that it can return the proper data on request

    Args:
        req (Request): Request containing the chain information.
        the body should contain
        - The chain name
        - Chain metadata
        - Chain data
    Returns:
        JSONResponse: Return a status object to the user indicating the new status of the
        chain
    """
    pass


@app.post(path="/v1/new_block/", status_code=201)
async def create_new_block(req: Request) -> JSONResponse:
    """Create a new

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
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
