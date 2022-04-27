import os


#   Database constants
MONGO_CONNECTION_STRING = f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@cluster0.yjy1g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DEFAULT_COLLECTION_NAME = "orphan_blocks"
DEFAULT_DATABASE_NAME = ""

#   Block constants

#   Blockchain constants
DEFAULT_CHAIN_NAME = "zchain"
DEFAULT_CHAIN_OWNER = "n0one"