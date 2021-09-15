# Import libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.users import add_code
import smtplib, ssl
import sqlite3
import random
import os


# Sends mail for resetting password to the user
def send_mail(path: str, email: str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # by importing os, backmail_add and backmail_pwd are accessing the environment variable values
    # backend_mail and backend_pwd are environment variables
    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    # Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(backemail_add, backemail_pwd)

    # Generates a 4 digit random verification code to verify the user while resetting the password
    key = random.randint(1000, 9999)
    # Inserts code into user table
    add_code(path, key, email)
    # print("VERIFICATION CODE:", key)
    # print("EMAIL:", email)

    # RESET URL
    url = "http://localhost:8000/reset"

    # user mail subject, body and format of the mail
    subject = "RESET YOUR PASSWORD:"
    body = f'Dear User\nPlease Click on the Link Below to Reset your "Code"Vid19 Password for your {email} account.\n\nThis is your 4 Digit Verification Code: {key} \n\nLink: {url} \n\nIf you didnt ask to reset your password please IGNORE this email!\n\nThank you\nWarm Regards\nTeam "Code"Vid19'
    msg = f"Subject: {subject}\n\n{body}"

    # Sends the mail with the data and quits the server
    server.sendmail(backemail_add, email, msg)
    server.quit()


# Sends the user an email with a reset link using html for the url
def send_link(path: str, email: str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # by importing os, backmail_add and backmail_pwd are accessing the environment variable values
    # backend_mail and backend_pwd are environment variables
    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    # Details to log into the server and the email id of the recepient
    sender_email = backemail_add
    receiver_email = email
    password = backemail_pwd

    # Uses a function to first generate the parts of the mail and then later combines them to form the mail
    message = MIMEMultipart("alternative")
    message["Subject"] = "RESET YOUR PASSWORD"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Generates a 4 digit random verification code to verify the user while resetting the password
    key = random.randint(1000, 9999)
    # Inserts code into user table
    add_code(path, key, email)
    # print("VERIFICATION CODE:", key)
    # print("EMAIL:", email)

    # Create the plain-text and HTML version of your message
    text = f"""\
    Dear User,
    Please follow this link to reset your "Code"Vid19 Password for the {email} account:
    This is your 4 Digit Verification Code: {key}
    http://localhost:8000/reset
    If you didnt ask to reset your password please IGNORE this email!
    Thank You,
    Warm Regards,
    Team "Code"Vid19
    """
    html = """\
    <html>
    <body>
        <p>
        Dear User,<br>
        Please follow this link to reset your "Code"Vid19 Password for the {{ email }} account: <br><br>
        <a href="http://localhost:8000/reset">Reset Password</a> <br><br>
        This is your 4 Digit Verification Code: {{ key }}<br><br>
        If you didnt ask to reset your password please IGNORE this email!<br><br>
        Thank You <br>
        Warm Regards <br>
        Team "Code"Vid19 <br>
        </p>
    </body>
    </html>
    """
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()


"""
Sends a mail to the user when the user buys a stock
Alerts the user with all the transaction details
"""


def send_buy(path: str, data: tuple):
    """
    symbol = data[0]
    price = data[1]
    quant = data[2]
    total = data[3]
    email = data[4]
    date = data[5]
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # by importing os, backmail_add and backmail_pwd are accessing the environment variable values
    # backend_mail and backend_pwd are environment variables
    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    # Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(backemail_add, backemail_pwd)

    # user mail subject, body and format of the mail
    subject = "Stock Transaction Receipt: IMP!"
    body = f'Dear User\nHere is your transaction receipt for your {data[4]} account.\n\nYou purchased {data[2]} units of the {data[0]} stock on {data[5]} at a rate of $ {data[1]} per stock unit.\n\nYour total expenditure was $ {data[3]}. Thank you for using "Code"vid19 Solutions.\n\nIf you did not make or authorize this transaction PLEASE CONTACT US IMMEDIATELY!\n\nThank you\nWarm Regards\nTeam "Code"Vid19'
    msg = f"Subject: {subject}\n\n{body}"

    # Sends the mail with the data and quits the server
    server.sendmail(backemail_add, data[4], msg)
    server.quit()


"""
Sends a mail to the user when the user sells a stock
Alerts the user with all the transaction details
"""


def send_sell(path: str, data: tuple):
    """
    symbol = data[0]
    price = data[1]
    quant = data[2]
    total = data[3]
    email = data[4]
    date = data[5]
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # by importing os, backmail_add and backmail_pwd are accessing the environment variable values
    # backend_mail and backend_pwd are environment variables
    backemail_add = os.environ.get("backend_mail")
    backemail_pwd = os.environ.get("backend_pwd")

    # Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(backemail_add, backemail_pwd)

    # user mail subject, body and format of the mail
    subject = "Stock Transaction Receipt: IMP!"
    body = f'Dear User\nHere is your transaction receipt for your {data[4]} account.\n\nYou sold {data[2]} units of the {data[0]} stock on {data[5]} at a rate of $ {data[1]} per stock unit.\n\nYour total earning was $ {data[3]}. Thank you for using "Code"vid19 Solutions.\n\nIf you did not make or authorize this transaction PLEASE CONTACT US IMMEDIATELY!\n\nThank you\nWarm Regards\nTeam "Code"Vid19'
    msg = f"Subject: {subject}\n\n{body}"

    # Sends the mail with the data and quits the server
    server.sendmail(backemail_add, data[4], msg)
    server.quit()


if __name__ == "__main__":
    # backemail_add = os.environ.get('backend_mail')
    # backemail_pwd = os.environ.get('backend_pwd')
    # print("EMAIL ID:", backemail_add)
    # print("PASSWORD:", backemail_pwd)
    # key = random.randint(1000,9999)
    # print(key)
    send_link("app.db", "ronaldo72emiway@gmail.com")
