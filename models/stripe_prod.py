import sqlite3 as s


def create_prod_table(path: str) -> None:
    """Creates prod_payment table in database

    Args:
        path: Path to database

    Returns:
            None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS prod_payment(Stock_Symbol TEXT, Prod_ID TEXT, Price_ID TEXT)"
    cur.execute(tbl)
    conn.commit()


def insert(path: str, tablename: str, data: tuple) -> None:
    """Inserts data into table when product and price are created

    Args:
        path: Path to database
        tablename: Tablename
        data: Data to be inserted

    Returns:
            None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    insrt = f"INSERT INTO {tablename} VALUES{data}"
    cur.execute(insrt)
    conn.commit()


def check_symbol(path: str, symbol: str) -> bool:
    """Checks if stock symbol is present in the table

    Args:
        path: Path to database
        symbol: Stock symbol to be checked

    Returns:
            bool
    """
    conn = s.connect(path)
    cur = conn.cursor()

    chk = f"SELECT * FROM prod_payment WHERE Stock_Symbol='{symbol}'"
    cur.execute(chk)
    res = cur.fetchall()
    if len(res) == 0:
        return False
    else:
        return True


def get_price_id(path: str, symbol: str) -> str:
    """Gets Price_ID for a particular symbol

    Args:
        path: Path to database
        symbol: Stock symbol

    Returns:
            str
    """
    conn = s.connect(path)
    cur = conn.cursor()

    cmnd = f"SELECT Price_ID FROM prod_payment WHERE Stock_Symbol='{symbol}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    print(res)
    return res[0][0]



def get_prod_id(path: str, symbol: str) -> str:
    """Gets Prod_ID for a particular symbol

    Args:
        path: Path to database
        symbol: Stock Symbol

    Returns:
            str
    """
    conn = s.connect(path)
    cur = conn.cursor()

    cmnd = f"SELECT Prod_ID FROM prod_payment WHERE Stock_Symbol='{symbol}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    print(res)
    return res[0][0]


def update_price_id(path: str, price_id: str, symbol: str) -> None:
    """Updates the price ID for a particular stock symbol

    Args:
        path: Path to database
        price_id: Price ID for that particular Stock Symbol
        symbol: Stock Symbol

    Returns:
            None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    upd = f"UPDATE prod_payment SET Price_ID='{price_id}' WHERE Stock_Symbol='{symbol}'"
    cur.execute(upd)
    conn.commit()


if __name__ == "__main__":
    pass
    # data = ("GOOGL", "prod_KDowNuIDvITlcA", "price_1JZNIGSAceEO9L8pPc6kkw1n")
    # insert("/home/nvombat/Desktop/Investment-WebApp/app.db", "prod_payment", data)
