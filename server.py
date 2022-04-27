__version__ = "1.0.0"
__author__ = "Zac Foteff"

import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from src.blockchain import Blockchain
from bin.constants import *
from bin.logger import Logger

app = FastAPI()
log = Logger("api")
chainCache = dict()
log("[-+-] Started listening for events at http://localhost:8000")

@app.get(path="/", status_code=200)
async def index() -> JSONResponse:
    """Root endpoint for blockchain interactions

    Returns:
        dict: JSON(ish) reponse that can be viewed in the browers, or postman, to
        confirm that the application is running
    """
    return JSONResponse(status_code=200, content={'status': 200, "response": "Thanks for navigating to the root endpoint of my blockchain api!"})

@app.get(path="/info/", status_code=200)
async def info_digest() -> JSONResponse:
    """Return a digest of information about the health of the server + the current state of
    the blockchain
    
    Returns:
        JSONResponse: Information digest of the health of the server
    """
    pass

@app.get(path="/chain/", status_code=200)
async def get_chain(req: Request) -> JSONResponse:
    """_summary_

    Args:
        req (Request): _description_
    Returns:
        JSONResponse: _description_
    """
    pass

@app.post(path="/v1/new_block/", status_code=201)
async def create_new_block(req: Request) -> JSONResponse:
    """Create a new

    Args:
        req (Request): HTTP request containing the new block's information. 
        The body should contain
        - Block value
        - Block proof
    Returns:
        JSONResponse: Status of block insertion into the chain. 201 if block is created,
        406 if the object cannot be created 
    """
    pass
