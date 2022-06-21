__version__ = "1.0.0"
__author__ = "Zac Foteff"

import time
import random
import string
import unittest

from server import app
from fastapi.testclient import TestClient

from bin.logger import Logger

log = Logger("apiTest")


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        return super().setUp()

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def test_get_root(self):
        start_time = time.perf_counter()
        response = self.client.get("/")
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], 200)
        self.assertEqual(
            response.json()["response"],
            "Thanks for navigating to the root endpoint of my blockchain api!",
        )
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed get root test in {elapsed_time:.5f}")


class TestAppCache(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        return super().setUp()

    def test_empty_cache(self):
        start_time = time.perf_counter()

        elapsed_time = time.perf_counter() - start_time
        log(
            f"[+] Completed test to ensure new objects are created with an empty cache in {elapsed_time:.5f}"
        )
