import smtplib,ssl
import os
import sqlite3
from models.users import add_code
import random

#backend_mail and backend_pwd are environt variables
#by importing os, backmail_add and backmail_pwd are accessing the environment variable values
def send_mail(email : str):

    conn= sqlite3.connect("app.db")
    cur = conn.cursor()

    backemail_add = os.environ.get('backend_mail')
    backemail_pwd = os.environ.get('backend_pwd')
    
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)

    key = random.randint(1000,9999)
    add_code(key, email)
    print("VERIFICATION CODE:", key)
    print("EMAIL:", email)

    #user mail subject, body and format of the mail
    subject = 'Reset Your Password:'
    body = f'Dear User\nPlease follow this link to reset your "Code"Vid19 Password for your {email} account.\n\n This is your 4 Digit Verification Code: {key} \n\n Link: \n\nIf you didnt ask to reset your password please IGNORE this email!\n\nThank you \n\nYour "Code"Vid19 Team'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(backemail_add,email,msg)
    server.quit()

    return key;

if __name__ == "__main__":
    backemail_add = os.environ.get('backend_mail')
    backemail_pwd = os.environ.get('backend_pwd')
    print("EMAIL ID:", backemail_add)
    print("PASSWORD:", backemail_pwd)
    key = random.randint(1000,9999)
    print(key)