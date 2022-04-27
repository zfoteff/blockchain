import time
import unittest
from bin.constants import *
from bin.logger import Logger
from src.block import Block
from src.blockchain import Blockchain

logger = Logger("./blockChain")


class TestBlockChain(unittest.TestCase):
    BLOCK_CHAIN_NAME = "btc"
    BLOCK_CHAIN_OWNER = "Zac"

    def test_not_null_blockchain(self) -> None:
        start_time = time.time()
        chain = Blockchain()
        self.assertIsNotNone(chain)
        self.assertIsInstance(chain, Blockchain)
        elapsed_time = time.time() - start_time
        logger.log(f"Completed block chain default values test in {elapsed_time:.3f} seconds. Created {chain}")


    def test_default_blockchain_values(self) -> None:
        start_time = time.time()
        chain = Blockchain()
        self.assertEqual(chain.name, DEFAULT_CHAIN_NAME)
        self.assertEqual(chain.owner, DEFAULT_CHAIN_OWNER)
        self.assertEqual(chain.chain, [])
        self.assertEqual(chain.pending_transactions, [])
        elapsed_time = time.time() - start_time
        logger.log(f"Completed block chain default values test in {elapsed_time:.3f} seconds. Created {chain}")


class TestProofOfWork(unittest.TestCase):
    def test_incorrect_proof(self) -> None:
        pass
