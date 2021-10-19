# Imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.users import add_code
import smtplib, ssl
import sqlite3
import random
import os


def send_mail(path: str, email: str) -> None:
    """Sends mail for resetting password to the user

    Args:
        path: Database path
        email: User email id

    Returns:
        None
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(backemail_add, backemail_pwd)

    key = random.randint(1000, 9999)
    add_code(path, key, email)

    url = "http://localhost:8000/reset"

    subject = "RESET YOUR PASSWORD:"
    body = f'Dear User\nPlease Click on the Link Below to Reset your "Code"Vid19 Password for your {email} account.\n\nThis is your 4 Digit Verification Code: {key} \n\nLink: {url} \n\nIf you didnt ask to reset your password please IGNORE this email!\n\nThank you\nWarm Regards\nTeam "Code"Vid19'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(backemail_add, email, msg)
    server.quit()


def send_buy(path: str, data: tuple) -> None:
    """Sends a mail to the user when the user buys stock

    Args:
        path: Database path
        data: Tuple with all transaction data
            symbol = data[0]
            price = data[1]
            quant = data[2]
            total = data[3]
            email = data[4]
            date = data[5]

    Returns:
        None
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(backemail_add, backemail_pwd)

    subject = "Stock Transaction Receipt: IMP!"
    body = f'Dear User\nHere is your transaction receipt for your {data[4]} account.\n\nYou purchased {data[2]} units of the {data[0]} stock on {data[5]} at a rate of $ {data[1]} per stock unit.\n\nYour total expenditure was $ {data[3]}. Thank you for using "Code"vid19 Solutions.\n\nIf you did not make or authorize this transaction PLEASE CONTACT US IMMEDIATELY!\n\nThank you\nWarm Regards\nTeam "Code"Vid19'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(backemail_add, data[4], msg)
    server.quit()


def send_sell(path: str, data: tuple) -> None:
    """Sends a mail to the user when the user sells stock

    Args:
        path: Database path
        data: Tuple with all transaction data
            symbol = data[0]
            price = data[1]
            quant = data[2]
            total = data[3]
            email = data[4]
            date = data[5]

    Returns:
        None
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(backemail_add, backemail_pwd)

    subject = "Stock Transaction Receipt: IMP!"
    body = f'Dear User\nHere is your transaction receipt for your {data[4]} account.\n\nYou sold {data[2]} units of the {data[0]} stock on {data[5]} at a rate of $ {data[1]} per stock unit.\n\nYour total earning was $ {data[3]}. Thank you for using "Code"vid19 Solutions.\n\nIf you did not make or authorize this transaction PLEASE CONTACT US IMMEDIATELY!\n\nThank you\nWarm Regards\nTeam "Code"Vid19'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(backemail_add, data[4], msg)
    server.quit()
