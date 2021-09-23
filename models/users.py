# Imports
import hashlib, binascii, os
from typing import Tuple
import sqlite3 as s


# Creates a user table
def create_user(path: str) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    # Command to create user table with 4 fields
    # EMAIL, NAME, PWD, CODE
    # CODE FIELD ONLY FOR RESET PASSWORD
    tbl = "CREATE TABLE IF NOT EXISTS user(Email TEXT, Name TEXT, Password TEXT, Code INT)"
    cur.execute(tbl)
    conn.commit()


# Inserts user and related values into table when a user is created
def insert(path: str, tablename: str, data: Tuple[str, str, str, int]) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    insrt = f"INSERT INTO {tablename} VALUES{data}"
    cur.execute(insrt)
    conn.commit()


# Checks password entered by user against the database
def checkpwd(path: str, pwd: str, email: str) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    # Queries table to fetch user with a particular password
    check = f"SELECT * FROM user where Password='{pwd}' AND Email='{email}'"
    cur.execute(check)
    # If query returns a match then passwords match
    res = cur.fetchall()
    if len(res) > 0:
        return True
    # If query results in an empty array then passwords dont match
    return False


# Checks if the RESET PASSWORD option and SIGN UP is possible by seeing if the user exists
def check_user_exist(path: str, email: str) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    # Queries the table to see if user with email id exists in the table for reset
    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    # Fetches results in array
    res = cur.fetchall()
    # If the array is empty then user doesnt exist and thus cant reset password but can sign up USER DOESNT EXIST
    if len(res) == 0:
        return False
    # If array is not empty - reset possible but signup not possible USER EXISTS
    else:
        return True


# Resets password for a particular user
def reset_pwd(path: str, pwd: str, code: int) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    # Updates the password for the particular user verified by the "CODE" sent to the users email id
    reset = f"UPDATE user SET Password='{pwd}' WHERE Code='{code}'"
    cur.execute(reset)
    conn.commit()


# Adds the verification code for the user when a reset password request is made
def add_code(path: str, key: int, email: str) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    # After requesting to reset password the user receives a mail with a link to reset and a verification code
    # This same code is added to the table so that when the user resets the password the user can be verified
    cmnd = f"UPDATE user SET Code='{key}' WHERE Email='{email}'"
    cur.execute(cmnd)
    conn.commit()


# Checks if the verification code given by the user matches the one sent to their email
def check_code(path: str, code: int) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    # Checks the table to see if the code matches the code that is stored for that particular user
    chk = f"SELECT * FROM user WHERE Code='{code}'"
    cur.execute(chk)
    res = cur.fetchall()
    # print("RES", res)
    # If code doesnt match then res will be empty
    if len(res) == 0:
        return False
    else:
        # Res array stores a tuple of the user details - code is the 4th field
        if res[0][3] == code:
            return True
        else:
            return False


# Resets the Verification code to 0 once the user has reset their password
# To avoid duplicate verification codes
def reset_code(path: str, code: int) -> None:
    conn = s.connect(path)
    cur = conn.cursor()

    # Updates the verification code to 0 wherever it matches a particular user verification code
    rstcd = f"UPDATE user SET Code=0 WHERE Code='{code}'"
    cur.execute(rstcd)
    conn.commit()


# Gets name of user
def getname(path: str, email: tuple) -> str:
    email = email[0]
    conn = s.connect(path)
    cur = conn.cursor()

    # Fetches name of particular user
    cmnd = f"SELECT Name FROM user WHERE Email='{email}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    return res[0][0]


# Fetches all the user emails from the user table
def getemail(path: str):
    conn = s.connect(path)
    cur = conn.cursor()

    gml = "SELECT Email FROM user"
    cur.execute(gml)
    emails = cur.fetchall()
    return emails


"""
For the contact us function:
If the user types a message and an email ID -
It checks if the email ID is in our database (the user exists)
It also checks if the email ID mentioned is the same one as the current user
If both these conditions are true the user is able to send a message otherwise an error message is displayed
"""


def check_contact_us(path: str, email: str, curr_user: str) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    # Command to fetch from the table any data with that particular email
    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    # Stores the fetched data in the table
    res = cur.fetchall()
    # print("RES", res)

    # Checks the above mentioned conditions
    if len(res) > 0 and res[0][0] == curr_user:
        return True
    else:
        return False


"""
Hashes the password entered by the user using the SHA256 HASH FUNCTION
First It generates salt using the urandom lib for CSPRNG
Then it converts the salt to hexadecimal and then encodes it in ASCII format
Then we use the Password based Key definition function which derives the secret key using the password and a HMAC pseudo-random function
It is also hashed with the salt and put through 100,000 iterations
binascii can convert between binary and ascii encoded binary representations
hexlify converts the binary data to hexadecimal
Final hash is computed with salt and then decoded to ascii and returned
"""


def hash_pwd(pwd: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    # print("SALT1: ", salt)
    pwd_hash = hashlib.pbkdf2_hmac("sha512", pwd.encode("utf-8"), salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    final_hashed_pwd = (salt + pwd_hash).decode("ascii")
    return final_hashed_pwd


"""
First we extract the stored hashed password from the database
Then from that we extract the password part and the salt part
We then hash the current password which the user has entered
We then compare the hashed password to the one stored in the db
if they match we return true else we return false
"""


def check_hash(path: str, pwd: str, email: str) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    # Command to fetch all data for user with a particular email id
    check = f"SELECT * FROM user where Email='{email}'"
    cur.execute(check)
    # Once the data is fetched from the db it is stored in a list
    res = cur.fetchall()
    # print("RES : ", res)
    # The list stores a tuple and password is the third element in the tuple
    dbpwd = res[0][2]
    # DATABASE STORED PASSWORD
    # print("DBPWD: ", dbpwd)

    # PASSWORD HASH AND SALT STORED IN DATABASE
    salt = dbpwd[:64]
    # print("SALT2: ", salt)
    dbpwd = dbpwd[64:]
    # print("Stored password hash: ", dbpwd)

    # PASSWORD HASH FOR PASSWORD THAT USER HAS CURRENTLY ENTERED
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha512", pwd.encode("utf-8"), salt.encode("ascii"), 100000
    )
    pwd_hash = binascii.hexlify(pwd_hash).decode("ascii")
    # print("pwd_hash: ", pwd_hash)

    if pwd_hash == dbpwd:
        return True
    else:
        return False


if __name__ == "__main__":
    test_path = "../test.db"
    create_user(test_path)
