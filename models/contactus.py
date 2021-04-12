import sqlite3 as s


#Creates the table in the database
def create_tbl(path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    #Command to create table if it doesnt exist
    tbl = 'CREATE TABLE IF NOT EXISTS contact_us(Email TEXT, Message TEXT)'
    cur.execute(tbl)
    conn.commit()


#Inserts message and email id from Contact_Us Page 
def insert(email : str, message : str, path : str):
    conn = s.connect(path)
    cur = conn.cursor()

    insrt = f"INSERT INTO contact_us VALUES('{email}','{message}')"
    cur.execute(insrt)
    conn.commit()