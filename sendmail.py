import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    body = f'Dear User\nPlease follow this link to reset your "Code"Vid19 Password for your {email} account.\n\n This is your 4 Digit Verification Code: {key} \n\n Link: <a href="../reset">Reset</a>\n\nIf you didnt ask to reset your password please IGNORE this email!\n\nThank you \n\nYour "Code"Vid19 Team'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(backemail_add,email,msg)
    server.quit()

    return key

def send_link(email : str):
    conn= sqlite3.connect("app.db")
    cur = conn.cursor()

    backemail_add = os.environ.get('backend_mail')
    backemail_pwd = os.environ.get('backend_pwd')

    sender_email = backemail_add
    receiver_email = email
    password = backemail_pwd

    message = MIMEMultipart("alternative")
    message["Subject"] = "RESET YOUR PASSWORD"
    message["From"] = sender_email
    message["To"] = receiver_email

    key = random.randint(1000,9999)
    add_code(key, email)
    print("VERIFICATION CODE:", key)
    print("EMAIL:", email)

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
        <p>Dear User,<br>
        Please follow this link to reset your "Code"Vid19 Password for the {email} account:<br><br>
        <a href="http://localhost:8000/reset">Reset Password</a> <br><br>
        This is your 4 Digit Verification Code: {key}<br><br>
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

if __name__ == "__main__":
    # backemail_add = os.environ.get('backend_mail')
    # backemail_pwd = os.environ.get('backend_pwd')
    # print("EMAIL ID:", backemail_add)
    # print("PASSWORD:", backemail_pwd)
    # key = random.randint(1000,9999)
    # print(key)
    send_link("ronaldo72emiway@gmail.com")