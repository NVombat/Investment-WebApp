import os
import unittest

from back import Currency_Conversion, get_current_stock_price
from dotenv import load_dotenv

from . import Base

data = Base()


class TestServer(unittest.TestCase):
    def test_stock_price(self):
        with self.assertWarns(ResourceWarning):
            try:
                assert (
                    type(get_current_stock_price(data.stock_data["stock_symbol"]))
                    == float
                )
            except Exception as e:
                return (False, str(e))

    def test_currency_conversion(self):
        load_dotenv()
        try:
            url = str.__add__(
                "http://data.fixer.io/api/latest?access_key=",
                os.getenv("CURRENCY_ACCESS_KEY"),
            )
        except Exception as e:
            return (False, str(e))
        c = Currency_Conversion(url)
        from_country = "USD"
        to_country = "INR"
        amount = 100
        assert type(c.convert(from_country, to_country, amount)) == float


if __name__ == "__main__":
    unittest.main()
