import sqlite3 as s


def create_user():
    conn = s.connect("app.db")
    cur = conn.cursor()

    tbl = 'CREATE TABLE IF NOT EXISTS user(Email TEXT, Name TEXT, Password TEXT, Code INT)'
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


def check_reset(email : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    res = cur.fetchall()
    if len(res)==0:
        return False
    else:
        return True


def reset_pwd(pwd : str, code : int):
    conn = s.connect("app.db")
    cur = conn.cursor()

    reset = f"UPDATE user SET Password='{pwd}' WHERE Code='{code}'"
    cur.execute(reset)
    conn.commit()


def add_code(key : int, email : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    cmnd = f"UPDATE user SET Code='{key}' WHERE Email='{email}'"
    cur.execute(cmnd)
    conn.commit()


def check_code(code : int):
    conn = s.connect("app.db")
    cur = conn.cursor()

    chk = f"SELECT * FROM user WHERE Code='{code}'"
    cur.execute(chk)
    res = cur.fetchall()
    print("RES", res)
    if res[0][3]==code:
        return True
    else:
        return False

def reset_code(code : int):
    conn = s.connect("app.db")
    cur = conn.cursor()

    rstcd = f"UPDATE user SET Code=0 WHERE Code='{code}'"
    cur.execute(rstcd)
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