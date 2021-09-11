import sqlite3 as s

def create_prod_table(path: str) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = 'CREATE TABLE IF NOT EXISTS prod_payment(Stock_Symbol TEXT, Prod_ID TEXT, Price_ID TEXT)'
    cur.execute(tbl)
    conn.commit()


#Inserts data into table when product and price are created
def insert(path: str, tablename: str, data: tuple) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    insrt = f'INSERT INTO {tablename} VALUES{data}'
    cur.execute(insrt)
    conn.commit()


# Checks if stock symbol is present in the table
def check_symbol(path: str, symbol: str) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()
    
    chk = f"SELECT * FROM prod_payment WHERE Stock_Symbol='{symbol}'"
    cur.execute(chk)
    # Fetches results in array
    res = cur.fetchall()
    # If the array is empty then symbol is not in table
    if len(res)==0:
        return False
    # If array is not empty then symbol is in table
    else:
        return True


# Gets Price ID
def get_price_id(path: str, symbol: str) -> str:
    conn = s.connect(path)
    cur = conn.cursor()

    cmnd = f"SELECT Price_ID FROM prod_payment WHERE Stock_Symbol='{symbol}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    print(res)
    return res[0][0]


# Gets Product ID
def get_prod_id(path: str, symbol: str) -> str:
    conn = s.connect(path)
    cur = conn.cursor()

    cmnd = f"SELECT Prod_ID FROM prod_payment WHERE Stock_Symbol='{symbol}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    print(res)
    return res[0][0]


# Udates Price ID
def update_price_id(path: str, price_id: str, symbol: str) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    upd = f"UPDATE prod_payment SET Price_ID='{price_id}' WHERE Stock_Symbol='{symbol}'"
    cur.execute(upd)
    conn.commit()