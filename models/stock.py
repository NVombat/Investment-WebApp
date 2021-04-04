import sqlite3 as s

def make_tbl():
    conn = s.connect("app.db")
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS stock(Date Date, Stock_Symbol Text, Price real, Quantity int)"
    cur.execute(tbl)
    conn.commit()

def buy(tablename : str, data : tuple):
    conn = s.connect("app.db")
    cur = conn.cursor()

    b = f"INSERT INTO {tablename} VALUES {data}"
    cur.execute(b)
    conn.commit()

def sell(tablename : str, sym : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    s = f"DELETE FROM {tablename} WHERE Stock_Symbol={sym}"
    cur.execute(s)
    conn.commit()
