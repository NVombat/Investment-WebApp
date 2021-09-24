import unittest
import sqlite3
import pytest
import os

import models.contactus as ct
import models.stock as st
import models.users as us

from . import Base
data = Base()


class TestDatabase(unittest.TestCase):
    def test_path(self):
        self.assertEqual("True", str(os.path.exists(data.contact_us_data["path"])))
        self.assertEqual("False", str(os.path.exists("apq.db")))


    def test_stock_data(self):
        assert type(data.stock_data["stock_symbol"]) == str
        assert type(data.stock_data["quantity"]) == int
        assert type(data.stock_data["price"]) == float


    def test_user_data(self):
        assert type(data.user_data["password"]) == str
        assert type(data.user_data["email"]) == str
        assert type(data.user_data["name"]) == str
        assert type(data.user_data["code"]) == int


    def test_data(self):
        assert type(data.contact_us_data["message"]) == str
        assert type(data.stock_data["date"]) == str
        assert type(data.user_data["path"]) == str


    def test_stock_buy(self):
        self.assertTrue(
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

        self.assertFalse(
            st.buy(
                data.test_data["tablename"],
                (
                    data.test_data["date"],
                    "XYZ",
                    data.test_data["price"],
                    data.test_data["quantity"],
                    data.test_data["email"],
                ),
                data.test_data["path"],
            )
        )

        with self.assertRaises(TypeError):
            st.buy(
                data.test_data["tablename"],
                (
                    data.test_data["date"],
                    1,
                    data.test_data["price"],
                    data.test_data["quantity"],
                    data.test_data["email"],
                ),
                data.test_data["path"],
            )


    def test_stock_sell(self):
        self.assertTrue(
            st.sell(
                data.test_data["tablename"],
                (
                    data.test_data["stock_symbol"],
                    data.test_data["quantity"],
                    data.test_data["email"],
                    data.test_data["price"],
                ),
                data.test_data["path"],
            )
        )

        self.assertFalse(
            st.sell(
                data.test_data["tablename"],
                (
                    data.test_data["stock_symbol"],
                    100,
                    data.test_data["email"],
                    data.test_data["price"],
                ),
                data.test_data["path"],
            )
        )

        self.assertFalse(
            st.sell(
                data.test_data["tablename"],
                (
                    "XYZ",
                    data.test_data["quantity"],
                    data.test_data["email"],
                    data.test_data["price"],
                ),
                data.test_data["path"],
            )
        )

        with self.assertRaises(TypeError):
            st.sell(
                data.test_data["tablename"],
                (
                    1,
                    data.test_data["quantity"],
                    data.test_data["email"],
                    data.test_data["price"],
                ),
                data.test_data["path"],
            )


    def test_stock_query(self):
        assert type(st.query(data.test_data["email"], data.test_data["path"])) == list


    def test_user_exists(self):
        assert us.check_user_exist(data.user_data["path"], data.user_data["email"]) == True
        assert us.check_user_exist(data.user_data["path"], data.test_data["email"]) == False


    def test_user_insert(self):
        self.assertIsNone(
            us.insert(
                data.test_data["path"],
                data.user_data["tablename"],
                (
                    data.test_data["email"],
                    data.test_data["name"],
                    data.test_data["password"],
                    data.test_data["code"],
                )
            )
        )

        with self.assertRaises(sqlite3.OperationalError):
            us.insert(
                data.test_data["path"],
                data.stock_data["tablename"],
                (
                    data.test_data["email"],
                    data.test_data["name"],
                    data.test_data["password"],
                    data.test_data["code"],
                )
            )


    def test_user_add_code(self):
        self.assertIsNone(
            us.add_code(
                data.test_data["path"],
                1000,
                data.test_data["email"]
            )
        )

        with self.assertRaises(TypeError):
            us.add_code(
                data.test_data["path"],
                '1000',
                data.test_data["email"]
            )


    def test_user_check_code(self):
        assert us.check_code(data.test_data["path"], 1000) == True
        assert us.check_code(data.test_data["path"], 4321) == False
        with self.assertRaises(TypeError):
            us.check_code(data.test_data["path"], '4321')


    def test_user_reset_code(self):
        with self.assertRaises(TypeError):
            us.reset_code(data.test_data["path"], '4321')


    def test_user_get_name(self):
        self.assertEqual(data.user_data["name"], us.getname(data.user_data["path"], (data.user_data["email"],)))
        self.assertNotEqual(data.test_data["name"], us.getname(data.user_data["path"], (data.user_data["email"],)))


    def test_user_get_emails(self):
        assert type(us.getemail(data.test_data["path"])) == list


if __name__ == "__main__":
    unittest.main()
