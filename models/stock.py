import sqlite3 as s


def make_tbl(path: str) -> None:
    """Creates the stock table in the database

    Args:
        path: Path to database

    Returns:
            None: Table is created if it doesnt already exist
    """
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS stock(Date Date, Stock_Symbol Text, Price real, Quantity int, Email Text)"
    cur.execute(tbl)
    conn.commit()


def buy(tablename: str, data: tuple, path: str) -> None:
    """Updates table when user BUYS stocks

    Args:
        tablename: Tablename
        data: Contains data related to transaction -> price, quantity, symbol etc.
        path: Path to database

    Returns:
            None
    """
    # print(tablename, data, path)
    conn = s.connect(path)
    cur = conn.cursor()

    # print("DATA:", data)
    # print("SYMBOL FROM TUPLE: ", data[1])
    # print("PRICE FROM TUPLE: ", data[2])
    # print("QUANTITY FROM TUPLE: ", data[3])
    # print("EMAIL FROM TUPLE: ", data[4])

    cmnd = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{data[1]}' AND Email='{data[4]}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    # If res is empty - User has not bought that particular stock thus insert into table as a new entry
    if len(res) == 0:
        b1 = f"INSERT INTO {tablename} VALUES {data}"
        cur.execute(b1)
        conn.commit()
        # print("INSERTED NEW INTO TABLE - NO PREVIOUS VALUES")
    # If res is not empty - User has already bought stocks with that symbol thus update the quantity of that particular stock
    else:
        b2 = f"UPDATE {tablename} SET Quantity=Quantity+'{data[3]}', Price='{data[2]}' WHERE Stock_Symbol = '{data[1]}' AND Email = '{data[4]}'"
        cur.execute(b2)
        conn.commit()
        # print("UPDATED VALUE IN TABLE - ALREADY EXISTED")


def sell(tablename: str, data: tuple, path: str) -> None:
    """Updates table when user SELLS stocks

    Args:
        tablename: Tablename
        data: Contains data related to transaction -> price, quantity, symbol etc.
        path: Path to database

    Returns:
            None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    # print("DATA: ", data)

    rem = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{data[0]}' AND Email = '{data[2]}'"
    cur.execute(rem)
    res = cur.fetchall()
    # print("SELLING RES: ", res)

    # If The user doesnt own that stock
    if len(res) == 0:
        print("YOU DO NOT OWN THIS STOCK")
    else:
        # Curr_Quant stores quantity of that particular stock the user owns currently
        curr_quant = int(res[0][3])
        # print(curr_quant)
        # Rejects request if user wants to sell more than the amount he owns
        if data[1] > curr_quant:
            print("YOU ARE TRYING TO SELL MORE THAN YOU OWN")
        # If user owns the same amount as the amount he wants to sell
        elif data[1] - curr_quant == 0:
            # Deletes the particular stock column from the table
            s1 = f"DELETE FROM {tablename} WHERE Stock_Symbol='{data[0]}' AND Email = '{data[2]}'"
            cur.execute(s1)
            conn.commit()
            # print("STOCK GONE - ALL SOLD")
        # Deducts the amount the user wants to sell from the amount the user owns
        else:
            s2 = f"UPDATE {tablename} SET Quantity=Quantity-'{data[1]}', Price='{data[3]}' WHERE Stock_Symbol='{data[0]}' AND Email = '{data[2]}'"
            cur.execute(s2)
            conn.commit()
            # print("SOLD - QUANTITY UPDATED")


def query(email: str, path: str) -> list:
    """Queries stock table to fetch all stocks purchased by a particular user

    Args:
        email: Email ID of user
        path: Path to database

    Returns:
            List: Containing all transactions made by the user
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
    print("TABLE CREATED...")
    print("BUYING...")
    print(buy("stock", ("19-9-2000", "NVDI", 354.9, 1, "test@gmail.com"), test_path))
    print(buy("stock", ("23-7-2002", "AAPL", 162.4, 2, "test@gmail.com"), test_path))
    print("SELLING...")
    print(sell("stock", ("NVDI", 1, "test@gmail.com", 354.9), test_path))
    print(sell("stock", ("AAPL", 2, "test@gmail.com", 162.4), test_path))
