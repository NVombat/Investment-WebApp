import unittest
import pytest

from back import (
    get_current_stock_price,
)

from . import Base

data = Base()


# class TestServer(unittest.TestCase):
#     def test_get_current_stock_price(self):
#         assert type(get_current_stock_price(data.stock_data["stock_symbol"])) == float
