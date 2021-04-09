import sqlite3 as s


def create_user():
    conn = s.connect("app.db")
    cur = conn.cursor()

    tbl = 'CREATE TABLE IF NOT EXISTS user(Email TEXT, Name TEXT, Password TEXT)'
    cur.execute(tbl)
    conn.commit()


def insert(tablename: str, data: tuple):
    conn = s.connect("app.db")
    cur = conn.cursor()

    insrt = f'INSERT INTO {tablename} VALUES{data}'
    cur.execute(insrt)
    conn.commit()


def checkpwd(pwd: str, email: str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    check = f"SELECT * FROM user where Password='{pwd}' AND Email='{email}'"
    cur.execute(check)
    res = cur.fetchall()
    if len(res) > 0:
        return True
    return False


def reset_pwd(tablename : str, pwd : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    reset = f"UPDATE {tablename} SET Password='{pwd}'" # WHERE Email='{email}'"
    cur.execute(reset)
    conn.commit()

def getname(email: tuple):
    email = email[0];
    conn = s.connect("app.db")

    cur = conn.cursor()
    cmnd = f"SELECT Name FROM user WHERE Email='{email}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    return res[0][0]


def getemail():
    conn = s.connect("app.db")
    cur = conn.cursor()

    gml = 'SELECT Email FROM user'
    cur.execute(gml)
    emails = cur.fetchall()
    return emails
