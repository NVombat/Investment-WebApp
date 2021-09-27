import unittest
import requests
import warnings
import pytest

from back import (
    get_current_stock_price,
)

from . import Base

data = Base()


class TestServer(unittest.TestCase):
    def test_stock_price(self):
        warnings.filterwarnings(
            action="ignore", message="unclosed", category=ResourceWarning
        )
        assert type(get_current_stock_price(data.stock_data["stock_symbol"])) == float


if __name__ == "__main__":
    unittest.main()
