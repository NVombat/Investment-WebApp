import sqlite3 as s

def make_tbl(path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS stock(Date Date, Stock_Symbol Text, Price real, Quantity int, Email Text)"
    cur.execute(tbl)
    conn.commit()

def buy(tablename : str, data : tuple, path : str):
    #print(tablename, data, path)
    conn = s.connect(path)
    cur = conn.cursor()

    #print("SYMBOL FROM TUPLE: ", data[1])
    #print("QUANTITY FROM TUPLE: ", data[3])

    cmnd = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{data[1]}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    if len(res)==0:
        b1 = f"INSERT INTO {tablename} VALUES {data}"
        cur.execute(b1)
        conn.commit()
        print("INSERTED NEW INTO TABLE - NO PREVIOUS VALUES")
    else:
        b2 = f"UPDATE {tablename} SET Quantity=Quantity+'{data[3]}' WHERE Stock_Symbol = '{data[1]}'"
        cur.execute(b2)
        conn.commit()
        print("UPDATED VALUE IN TABLE - ALREADY EXISTED")

def sell(tablename : str, sym : str, quant : int, path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    rem = f"SELECT * FROM {tablename} WHERE Stock_Symbol='{sym}'"
    cur.execute(rem)
    res = cur.fetchall()
    print("SELLING RES: ", res)

    if len(res)==0:
        print("YOU DO NOT OWN THIS STOCK")
    else:
        curr_quant = int(res[0][3])
        print(curr_quant)
        if quant > curr_quant:
            print("YOU ARE TRYING TO SELL MORE THAN YOU OWN")
        elif quant-curr_quant==0:
            s1 = f"DELETE FROM {tablename} WHERE Stock_Symbol='{sym}'"
            cur.execute(s1)
            conn.commit()
            print("STOCK GONE - ALL SOLD")
        else:
            s2 = f"UPDATE {tablename} SET Quantity=Quantity-'{quant}' WHERE Stock_Symbol='{sym}'"
            cur.execute(s2)
            conn.commit()
            print("SOLD - QUANTITY UPDATED")

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

