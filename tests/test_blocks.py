import random
import time
import unittest
from bin.constants import *
from bin.logger import Logger
from src.block import Block

logger = Logger("./block")


class TestBlocks(unittest.TestCase):
    def test_not_null_block(self) -> None:
        start_time = time.time()
        block = Block()
        self.assertIsNotNone(block)
        self.assertIsInstance(block, Block)
        elapsed_time = time.time() - start_time
        logger.log(f"Completed block instance test in {elapsed_time:.3f} seconds")

    def test_default_block_values(self) -> None:
        start_time = time.time()
        block = Block()
        self.assertEqual(block.index, 0)
        self.assertEqual(block.value, {})
        self.assertEqual(block.proof, 0.0)
        self.assertEqual(block.prev_hash, None)
        elapsed_time = time.time() - start_time
        logger.log(
            f"Completed block default values test in {elapsed_time:.3f} seconds. Created {block}"
        )

    def test_block_constructor(self) -> None:
        start_time = time.time()
        test_index = random.randint(0, 100)
        test_value = {"seller": "Bob", "buyer": "Alice", "amount": 100}
        test_proof = random.random()
        block = Block(index=test_index, value=test_value, proof=test_proof)
        self.assertIsNotNone(block)
        self.assertEqual(block.index, test_index)
        self.assertEqual(block.value, test_value)
        self.assertEqual(block.proof, test_proof)
        elapsed_time = time.time() - start_time
        logger.log(
            f"Completed block constructor values test in {elapsed_time:.3f} seconds. Created {block}"
        )
