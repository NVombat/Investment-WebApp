import sqlite3 as s

def create_prod_table(path: str) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = 'CREATE TABLE IF NOT EXISTS prod_payment(Stock_Symbol TEXT, Prod_ID TEXT, Price_ID TEXT)'
    cur.execute(tbl)
    conn.commit()

    

