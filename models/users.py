import sqlite3 as s


#Creates a user table 
def create_user():
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Command to create user table with 4 fields
    #EMAIL, NAME, PWD, CODE
    #CODE FIELD ONLY FOR RESET PASSWORD 
    tbl = 'CREATE TABLE IF NOT EXISTS user(Email TEXT, Name TEXT, Password TEXT, Code INT)'
    cur.execute(tbl)
    conn.commit()


#Inserts user and related values into table when a user is created
def insert(tablename: str, data: tuple):
    conn = s.connect("app.db")
    cur = conn.cursor()

    insrt = f'INSERT INTO {tablename} VALUES{data}'
    cur.execute(insrt)
    conn.commit()


#Checks password entered by user against the database
def checkpwd(pwd: str, email: str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Queries table to fetch user with a particular password
    check = f"SELECT * FROM user where Password='{pwd}' AND Email='{email}'"
    cur.execute(check)
    #If query returns a match then passwords match
    res = cur.fetchall()
    if len(res) > 0:
        return True
    #If query results in an empty array then passwords dont match
    return False


#Checks if the RESET PASSWORD option and SIGN UP is possible by seeing if the user exists
def check_user_exist(email : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Queries the table to see if user with email id exists in the table for reset
    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    #Fetches results in array
    res = cur.fetchall()
    #If the array is empty then user doesnt exist and thus cant reset password but can sign up
    if len(res)==0:
        return False
    #If array is not empty - reset possible but signup not possible
    else:
        return True


#Resets password for a particular user
def reset_pwd(pwd : str, code : int):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Updates the password for the particular user verified by the "CODE" sent to the users email id
    reset = f"UPDATE user SET Password='{pwd}' WHERE Code='{code}'"
    cur.execute(reset)
    conn.commit()


#Adds the verification code for the user when a reset password request is made
def add_code(key : int, email : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #After requesting to reset password the user receives a mail with a link to reset and a verification code
    #This same code is added to the table so that when the user resets the password the user can be verified
    cmnd = f"UPDATE user SET Code='{key}' WHERE Email='{email}'"
    cur.execute(cmnd)
    conn.commit()


#Checks if the verification code given by the user matches the one sent to their email
def check_code(code : int):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Checks the table to see if the code matches the code that is stored for that particular user
    chk = f"SELECT * FROM user WHERE Code='{code}'"
    cur.execute(chk)
    res = cur.fetchall()
    print("RES", res)
    #Res array stores a tuple of the user details - code is the 4th field
    if res[0][3]==code:
        return True
    else:
        return False


#Resets the Verification code to 0 once the user has reset their password
#To avoid duplicate verification codes
def reset_code(code : int):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Updates the verification code to 0 wherever it matches a particular user verification code
    rstcd = f"UPDATE user SET Code=0 WHERE Code='{code}'"
    cur.execute(rstcd)
    conn.commit()


#Gets name of user
def getname(email: tuple):
    email = email[0];
    conn = s.connect("app.db")

    #Fetches name of particular user
    cur = conn.cursor()
    cmnd = f"SELECT Name FROM user WHERE Email='{email}'"
    cur.execute(cmnd)
    res = cur.fetchall()
    return res[0][0]


#Fetches all the user emails from the user table
def getemail():
    conn = s.connect("app.db")
    cur = conn.cursor()

    gml = 'SELECT Email FROM user'
    cur.execute(gml)
    emails = cur.fetchall()
    return emails


'''
For the contact us function:
If the user types a message and an email ID - 
It checks if the email ID is in our database (the user exists)
It also checks if the email ID mentioned is the same one as the current user
If both these conditions are true the user is able to send a message otherwise an error message is displayed
'''
def check_contact_us(email : str, curr_user : str):
    conn = s.connect("app.db")
    cur = conn.cursor()

    #Command to fetch from the table any data with that particular email
    chk = f"SELECT * FROM user WHERE Email='{email}'"
    cur.execute(chk)
    #Stores the fetched data in the table
    res = cur.fetchall()
    print("RES", res)

    #Checks the above mentioned conditions
    if len(res)>0 and res[0][0]==curr_user:
        return True
    else:
        return False