import unittest
import pytest
import os

import models.contactus as ct
import models.stock as st
import models.users as us

from .test_data import Base

data = Base()


class TestDatabase(unittest.TestCase):
    def test_path(self):
        self.assertEqual("True", str(os.path.exists(data.contact_us_data["path"])))
        self.assertEqual("False", str(os.path.exists("apq.db")))

    def test_stock_buy(self):
        self.assertIsNone(
            st.buy(
                data.test_data["tablename"],
                (
                    data.test_data["date"],
                    data.test_data["stock_symbol"],
                    data.test_data["price"],
                    data.test_data["quantity"],
                    data.test_data["email"],
                ),
                data.test_data["path"],
            )
        )

        # ADD CHECK TO REFUSE ANYTHING BUT INT
        # self.assertIsNone(st.buy(data.test_data["tablename"],
        #                 (data.test_data["date"], "XYZ",
        #                 data.test_data["price"], "quant",
        #                 data.test_data["email"]), data.test_data['path']))

    def test_users_(self):
        pass


if __name__ == "__main__":
    unittest.main()
