import sqlite3 as s

def make_tbl(path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS stock(Date Date, Stock_Symbol Text, Price real, Quantity int, Email Text)"
    cur.execute(tbl)
    conn.commit()

def buy(tablename : str, data : tuple, path : str):
    print(tablename, data, path)
    conn = s.connect(path)
    cur = conn.cursor()

    b = f"INSERT INTO {tablename} VALUES {data}"
    cur.execute(b)
    conn.commit()

def sell(tablename : str, sym : str, path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    rem = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{sym}'"
    cur.execute(rem)
    res = cur.fetchall()
    quant = res[0][4]
    print(quant)
    print(res)
    
    sel = f"DELETE FROM {tablename} WHERE Stock_Symbol='{sym}'"
    cur.execute(sel)
    conn.commit()

def query(email : str, path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    que = f"SELECT * FROM stock WHERE Email ='{email}'"
    cur.execute(que)
    res = cur.fetchall()
    return res

if __name__ == "__main__":
    path = "../app.db"
    make_tbl("../app.db")
    buy("stock", ("19-9-2000", "GOOGL", 354.9, 14, "ronaldo72emiway@gmail.com"), path)
    buy("stock", ("23-7-2002", "AAPL", 162.4, 10, "ronaldo72emiway@gmail.com"), path)

