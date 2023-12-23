import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename="local.env"))

#   Default
DEFAULT_CHAIN_NAME = "zchain"
DEFAULT_CHAIN_OWNER = "n0one"
DEFAULT_DATABASE_NAME = "chain_data"
DEFAULT_COLLECTION_NAME = "orphan_blocks"

#   Local Database Constants
MONGO_USER = os.environ["MONGO_HOST"]
MONGO_PASSWORD = os.environ["MONGO_PORT"]
MONGO_URL = os.environ["MONGO_URL"]

