import unittest
import requests
import warnings
import pytest
import os

from back import get_current_stock_price, Currency_Conversion
from dotenv import load_dotenv
from . import Base

data = Base()


class TestServer(unittest.TestCase):
    def test_stock_price(self):
        warnings.filterwarnings(
            action="ignore", message="unclosed", category=ResourceWarning
        )
        assert type(get_current_stock_price(data.stock_data["stock_symbol"])) == float

    def test_currency_conversion(self):
        load_dotenv()
        try:
            url = str.__add__(
                "http://data.fixer.io/api/latest?access_key=",
                os.getenv("CURRENCY_ACCESS_KEY"),
            )
        except Exception as e:
            print("Error")
            return False
        c = Currency_Conversion(url)
        from_country = "USD"
        to_country = "INR"
        amount = 100
        assert type(c.convert(from_country, to_country, amount)) == float


if __name__ == "__main__":
    unittest.main()
