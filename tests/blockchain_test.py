__version__ = "1.0.0"
__author__ = "Zac Foteff"

import time
import unittest

from resources.constants import *
from resources.logger import Logger
from src.block import Block
from src.blockchain import Blockchain

log = Logger("blockchain_test")


class TestBlockChain(unittest.TestCase):
    BLOCK_CHAIN_NAME = "btc"
    BLOCK_CHAIN_OWNER = "Zac"

    def test_not_null_blockchain(self) -> None:
        start_time = time.perf_counter()
        chain = Blockchain()
        self.assertIsNotNone(chain)
        self.assertIsInstance(chain, Blockchain)
        elapsed_time = time.perf_counter() - start_time
        log(
            f"Completed block chain default values test in {elapsed_time:.3f} seconds. Created {chain}"
        )

    def test_default_blockchain_values(self) -> None:
        start_time = time.perf_counter()
        chain = Blockchain()
        self.assertEqual(chain.name, DEFAULT_CHAIN_NAME)
        self.assertEqual(chain.owner, DEFAULT_CHAIN_OWNER)
        self.assertEqual(chain.pending_transactions, [])
        elapsed_time = time.perf_counter() - start_time
        log(
            f"Completed block chain default values test in {elapsed_time:.3f} seconds. Created {chain}"
        )

    def test_blockchain_constructor(self) -> None:
        start_time = time.perf_counter()
        test_chain_name = "TestChain"
        test_chain_owner = "test owner"
        chain = Blockchain(test_chain_name, test_chain_owner)
        self.assertEqual(chain.name, test_chain_name)
        self.assertEqual(chain.owner, test_chain_owner)
        self.assertEqual(chain.pending_transactions, [])
        elapsed_time = time.perf_counter() - start_time
        log(
            f"Completed block chain default values test in {elapsed_time:.3f} seconds. Created {chain}"
        )

    def test_genesis_block_existance(self) -> None:
        start_time = time.perf_counter()
        test_chain_name = "TestChain"
        test_chain_owner = "test owner"
        chain = Blockchain(name=test_chain_name, owner=test_chain_owner)
        self.assertIsNotNone(chain.chain)
        self.assertIsNotNone(chain.chain[0])
        chain = Blockchain(test_chain_name, test_chain_owner)
        elapsed_time = time.perf_counter() - start_time
        log(
            f"Completed block chain genesis block existance test in {elapsed_time:.3f} seconds. Created {chain}"
        )

    def test_persist_chain_in_database(self) -> None:
        start_time = time.perf_counter()
        chain = Blockchain(self.BLOCK_CHAIN_NAME, self.BLOCK_CHAIN_OWNER)
        elapsed_time = time.perf_counter() - start_time
        log(f"Completed blockchain persistance test{elapsed_time:.3f}")


class TestProofOfWork(unittest.TestCase):
    def test_incorrect_proof(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
