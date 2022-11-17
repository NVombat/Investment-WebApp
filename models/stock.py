import io
import sqlite3 as s
from typing import Tuple

import pandas as pd
import requests

# List of stock symbols from URL containing NASDAQ listings
url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
data = requests.get(url).content
df_data = pd.read_csv(io.StringIO(data.decode("utf-8")))
symbols = df_data["Symbol"].to_list()


def make_tbl(path: str) -> None:
    """Creates the stock table in the database

    Args:
        path: Path to database

    Returns:
        None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS stock(Date Date, Stock_Symbol Text, Price real, Quantity int, Email Text)"
    cur.execute(tbl)
    conn.commit()


def buy(tablename: str, data: Tuple[str, str, float, int, str], path: str) -> bool:
    """Updates table when user BUYS stocks

    Args:
        tablename: Tablename
        data: Transaction data
        path: Path to database

    Returns:
        bool
    """
    if not (isinstance(data[1], str)):
        raise TypeError("Invalid Type")

    elif data[1].upper() in symbols:
        conn = s.connect(path)
        cur = conn.cursor()

        cmnd = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{data[1]}' AND Email='{data[4]}'"
        cur.execute(cmnd)
        res = cur.fetchall()

        if len(res) == 0:
            b1 = f"INSERT INTO {tablename} VALUES {data}"
            cur.execute(b1)
            conn.commit()
            return True

        else:
            b2 = f"UPDATE {tablename} SET Quantity=Quantity+'{data[3]}', Price='{data[2]}' WHERE Stock_Symbol = '{data[1]}' AND Email = '{data[4]}'"
            cur.execute(b2)
            conn.commit()
            return True
    else:
        return False


def sell(tablename: str, data: Tuple[str, int, str, float], path: str) -> bool:
    """Updates table when user SELLS stocks

    Args:
        tablename: Tablename
        data: Transaction data
        path: Path to database

    Returns:
        bool
    """
    if not (isinstance(data[0], str)):
        raise TypeError("Invalid Type")

    elif data[0].upper() in symbols:
        conn = s.connect(path)
        cur = conn.cursor()

        rem = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{data[0]}' AND Email = '{data[2]}'"
        cur.execute(rem)
        res = cur.fetchall()

        if len(res) == 0:
            return False
        else:
            curr_quant = int(res[0][3])
            if data[1] > curr_quant:
                return False

            elif data[1] - curr_quant == 0:
                s1 = f"DELETE FROM {tablename} WHERE Stock_Symbol='{data[0]}' AND Email = '{data[2]}'"
                cur.execute(s1)
                conn.commit()
                return True

            else:
                s2 = f"UPDATE {tablename} SET Quantity=Quantity-'{data[1]}', Price='{data[3]}' WHERE Stock_Symbol='{data[0]}' AND Email = '{data[2]}'"
                cur.execute(s2)
                conn.commit()
                return True
    else:
        return False


def query(email: str, path: str) -> list:
    """Fetch all stocks purchased by a particular user

    Args:
        email: User Email ID
        path: Path to database

    Returns:
        List
    """
    conn = s.connect(path)
    cur = conn.cursor()

    que = f"SELECT * FROM stock WHERE Email ='{email}'"
    cur.execute(que)
    res = cur.fetchall()
    return res


if __name__ == "__main__":
    test_path = "../test.db"
    print(make_tbl(test_path))
    print(buy("stock", ("19-9-2000", "NVDI", 354.9, 1, "test@gmail.com"), test_path))
    print(buy("stock", ("23-7-2002", "AAPL", 162.4, 2, "test@gmail.com"), test_path))
    print(sell("stock", ("NVDI", 1, "test@gmail.com", 354.9), test_path))
    print(sell("stock", ("AAPL", 2, "test@gmail.com", 162.4), test_path))
