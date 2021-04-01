import sqlite3 as s

def create_tbl(path : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    tbl = 'CREATE TABLE IF NOT EXISTS contact_us(Email TEXT, Message TEXT)'
    cur.execute(tbl)
    conn.commit()

def insert(email : str, message : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    insrt = f"INSERT INTO contact_us VALUES('{email}','{message}')"
    cur.execute(insrt)
    conn.commit()