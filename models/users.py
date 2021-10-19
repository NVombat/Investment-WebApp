# Imports
import hashlib, binascii, os
from typing import Tuple
import sqlite3 as s


def create_user(path: str) -> None:
    """Creates user table in the database

    Args:
        path: Path to database

    Returns:
        None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS user(Email TEXT, Name TEXT, Password TEXT, Code INT)"
    cur.execute(tbl)
    conn.commit()


def insert(path: str, tablename: str, data: Tuple[str, str, str, int]) -> None:
    """Inserts user and related values into table

    Args:
        path: Path to database
        tablename: Tablename
        data: User data

    Returns:
        None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    insrt = f"INSERT INTO {tablename} VALUES{data}"
    cur.execute(insrt)
    conn.commit()


def check_user_exist(path: str, email: str) -> bool:
    """Checks if user exists in database

    Args:
        path: Path to database
        email: User email id

    Returns:
        bool
    """
    conn = s.connect(path)
    cur = conn.cursor()

    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    res = cur.fetchall()

    if len(res) == 0:
        return False
    else:
        return True


def reset_pwd(path: str, pwd: str, code: int) -> None:
    """Resets password for a particular user

    Args:
        path: Path to database
        pwd: Current user password
        code: Verification code

    Returns:
        None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    reset = f"UPDATE user SET Password='{pwd}' WHERE Code='{code}'"
    cur.execute(reset)
    conn.commit()


def add_code(path: str, key: int, email: str) -> None:
    """Adds verification code for user

    Args:
        path: Path to database
        key: Verification code
        email: User email id

    Returns:
        None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    if isinstance(key, int):
        cmnd = f"UPDATE user SET Code='{key}' WHERE Email='{email}'"
        cur.execute(cmnd)
        conn.commit()
    else:
        raise TypeError


def check_code(path: str, code: int) -> bool:
    """Checks if verification code is valid

    Args:
        path: Path to database
        code: Verification code

    Returns:
        bool
    """
    conn = s.connect(path)
    cur = conn.cursor()

    if isinstance(code, int):
        chk = f"SELECT * FROM user WHERE Code='{code}'"
        cur.execute(chk)
        res = cur.fetchall()

        if len(res) == 0:
            return False
        else:
            if res[0][3] == code:
                return True
            else:
                return False
    else:
        raise TypeError


def reset_code(path: str, code: int) -> None:
    """Resets the Verification code to 0

    Args:
        path: Path to database
        code: Verification code

    Returns:
        None
    """
    conn = s.connect(path)
    cur = conn.cursor()

    if isinstance(code, int):
        rstcd = f"UPDATE user SET Code=0 WHERE Code='{code}'"
        cur.execute(rstcd)
        conn.commit()
    else:
        raise TypeError


def getname(path: str, email: tuple) -> str:
    """Gets name of user

    Args:
        path: Path to database
        email: User email id

    Returns:
        str
    """
    email = email[0]
    conn = s.connect(path)
    cur = conn.cursor()

    cmnd = f"SELECT Name FROM user WHERE Email='{email}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    return res[0][0]


def getemail(path: str):
    """Gets all user emails from table

    Args:
        path: Path to database
    """
    conn = s.connect(path)
    cur = conn.cursor()

    gml = "SELECT Email FROM user"
    cur.execute(gml)
    emails = cur.fetchall()
    return emails


def check_contact_us(path: str, email: str, curr_user: str) -> bool:
    """Checks if email is in database and is also the current user
    This is to allow the user to "contact_us"

    Args:
        path: Path to database
        email: User email id
        curr_user: User in session

    Returns:
        bool
    """
    conn = s.connect(path)
    cur = conn.cursor()

    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    res = cur.fetchall()

    if len(res) > 0 and res[0][0] == curr_user:
        return True
    else:
        return False


def hash_pwd(pwd: str) -> str:
    """Hashes password using salted password hashing

    Args:
        pwd: Password to be hashed

    Returns:
        str
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    pwd_hash = hashlib.pbkdf2_hmac("sha512", pwd.encode("utf-8"), salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    final_hashed_pwd = (salt + pwd_hash).decode("ascii")
    return final_hashed_pwd


def check_hash(path: str, pwd: str, email: str) -> bool:
    """Verifies password with hashed database password

    Args:
        path: Path to database
        pwd: Password
        email: User email id

    Returns:
        bool
    """
    conn = s.connect(path)
    cur = conn.cursor()

    check = f"SELECT * FROM user where Email='{email}'"
    cur.execute(check)
    res = cur.fetchall()

    dbpwd = res[0][2]
    salt = dbpwd[:64]
    dbpwd = dbpwd[64:]

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha512", pwd.encode("utf-8"), salt.encode("ascii"), 100000
    )
    pwd_hash = binascii.hexlify(pwd_hash).decode("ascii")

    if pwd_hash == dbpwd:
        return True
    else:
        return False


if __name__ == "__main__":
    test_path = "../test.db"
    create_user(test_path)
    insert(test_path, "user", ("test2@gmail.com", "Karan", "test456", 1111))
    add_code(test_path, 1234, "test@gmail.com")
    reset_pwd(test_path, "test456", 1111)
    reset_pwd(test_path, "test123", 1234)
