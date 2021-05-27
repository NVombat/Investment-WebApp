# Imports all the flask libraries
from flask import (
    Flask,
    session,
    g,
    render_template,
    request,
    redirect,
    url_for
)


# Other libraries needed
import datetime as d
import numpy as np
import requests
import json
import os


# Imports functions from other folders
from sendmail import send_mail, send_buy, send_sell
from models import users, contactus, stock
from api import getdata


# Path used for all tables
path = "app.db"


templates_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=templates_path)
app.secret_key = 'somekey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Creates all the tables when the website is run
users.create_user()
contactus.create_tbl(path)
stock.make_tbl(path)


'''
Sets the current user - g.user to none and then checks if the user is in session
If the user is in session then their email is fetched and g.user is updated to that email
Otherwise Exception is thrown
'''
@app.before_request
def security():
    g.user = None
    if 'user_email' in session:
        emails = users.getemail()
        try:
            useremail = [email for email in emails if email[0] == session['user_email']][0]
            g.user = useremail
        except Exception as e:
            print("Failed")


# LOGIN page
@app.route('/', methods=["GET", "POST"])
def home():
    # The particular user is removed from session
    session.pop("user_email", None)

    # Flag checks if the password entered by the user is correct or not
    flag = True

    """
    If a post request is made on the login page
    Take input from the fields - Name, Email, Password, Confirm Password
    """
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['rpassword']

        '''
        If the password field has a password, and the repeat password is empty the user is trying to login
        First the user is verified -> Check if user exists
        Then the password is verified by checking the database for that user
        If the password matches the user is added to the session otherwise the flag variable is set to false
        If the user doesnt exist then render back to login and give error message
        '''
        if password and not repeat_password:
            if users.check_user_exist(email):
                print("Login")
                # if users.checkpwd(password, email):
                #     session['user_email'] = email
                #     return redirect('/index')
                '''
                If the password field is entered check the password againts the hashed password in the db
                If it matches then user is in session and is redirected to the homepage
                Else a flag is set and the user is shown an error message
                '''
                if users.check_hash(password, email):
                    session['user_email'] = email
                    return redirect('/index')
                else:
                    #If the flag variable is false -> user has entered the wrong password
                    flag = False
                    print("WRONG PWD")
                    #And is redirected to the login page
                    return render_template('login.html', error="Incorrect Password")
            else:
                #If the user doesnt exist
                return render_template('login.html', error="User Doesnt Exist")

        '''
        If the password and repeat password fields are filled - SIGN UP
        If the user already exists then print an error message and redirect to login page
        If the user doesnt exist then allow the signup to take place
        If they both are the same (password and repeat password)
        Then a new user is added to the USER TABLE in the database with all the data
        The user is then added to the session and the user is redirected to the login page
        If the fields dont match the user is alerted and redirected back to the login page to try again
        '''
        if password and repeat_password:
            print("Sign Up")
            if not users.check_user_exist(email):
                if password == repeat_password:
                    #Hash the users password and store the hashed password for security
                    password = users.hash_pwd(password)
                    print("Hashed PWD: ", password)
                    users.insert('user', (email, name, password, 0))
                    print("Inserted Hashed Password")
                    session['user_email'] = email
                    return render_template('login.html', error="Sign Up Complete - Login")
                else:
                    return render_template('login.html', error="Password & Retyped Password Not Same")
            else:
                return render_template('login.html', error="This User Already Exists! Try Again")

        '''
        If only the email field is filled it means the user has requested to reset their password
        First the User table is looked up to see if the user exists (if the password can be reset)
        The password is reset if the user exists through the reset process (mail, verification code ...)
        If the user doesnt exist an error message is generated and the user is redirected back to the login page
        '''
        if not name and not password and email:
            if users.check_user_exist(email):
                print("Reset Password:")
                # session['user_email'] = email
                reset_password(email)
                return render_template('login.html',
                                       error="We have sent you a link to reset your password. Check your mailbox")
            else:
                print("User Doesnt Exist")
                return render_template('login.html', error="This Email Doesnt Exist - Please Sign Up")

    #If the flag variable is true then the user has entered the correct password and is redirected to the login page
    #FLAG VALUE IS TRUE INITIALLY
    if flag:
        return render_template('login.html')    


# HOME page
@app.route('/index', methods=["GET", "POST"])
def index():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template("index.html")
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect('/')


"""
Function to reset password
Sends the mail for resetting password to user
"""
def reset_password(email: str):
    print(email)
    send_mail(email)


# RESET PASSWORD page
@app.route('/reset', methods=["GET", "POST"])
def reset():
    """
    Once the user clicks on the reset password link sent to his mail he is taken to the reset password page
    If a post request is generated (when user clicks submit) - all the input fields are fetched (pwd, rpwd, code)
    If all three fields are filled it checks if the password and repeat password match
    If the two passwords match the verification code is checked in the database to verify user
    If code matches the user then the password is updated for the user in the database 
    The code is set back to 0 for that user (to avoid repetition of codes)
    Otherwise an error is generated
    """
    if request.method == "POST":
        pwd = request.form['npassword']
        repeat_pwd = request.form['rnpassword']
        ver_code = request.form['vcode']
        ver_code = int(ver_code)
        print(ver_code)

        if pwd and repeat_pwd and ver_code:
            print("CHECKING")
            if pwd == repeat_pwd:
                if users.check_code(ver_code):
                    #Hash the new password and update db with hashed password
                    pwd = users.hash_pwd(pwd)
                    users.reset_pwd(pwd, ver_code)
                    print("Resetting password & Updating DB")
                    users.reset_code(ver_code)
                    return redirect("/")
                    # return render_template('login.html', error="Password Reset Successfully")
                else:
                    print("Verification Code Doesnt Match")
                    return redirect("/")
                    # return render_template('login.html', error="Try resetting again")
            else:
                return render_template('reset.html', error="Password & Retyped Password Not Same")
    return render_template('reset.html')


# ANALYSIS page
@app.route('/inv')
def inv():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template('inv.html')
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect('/')


# ABOUT US page
@app.route('/about')
def about():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template('about.html')
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect('/')


# TRADING GUIDE page
@app.route('/doc')
def doc():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template('doc.html')
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect('/')


# TRADE page
@app.route('/trade', methods=["GET", "POST"])
def trade():
    # Enters the page only if a user is signed in - g.user represents the current user
    print(g.user)
    if g.user:

        '''
        uses the user email id to query the users transactions
        this transactions array is then received by the table on the html page
        '''
        user_email = g.user
        transactions = stock.query(user_email[0], path)

        if request.method == "POST":

            '''
            If a post request is generated (button clicked) the user wants to buy or sell stocks
            It is then checked whether the user wants to buy or sell (based on the button pressed)
            '''
            # BUYING
            if request.form.get("b1"):
                # The data from the fields on the page are fetched
                symb = request.form["stockid"]
                quant = request.form["amount"]

                '''
                If both the fields had data then the current date and time is first calculated
                Then the quantity is stored as an integer
                The stock price api is called to calculate the price of that particular stock
                The total amount of money spent is then calculated using price and quantity
                The STOCK TABLE is then updated with this data using the buy function
                A mail is sent to the user alerting them of the transaction made
                The user is now redirected back to the trade page - we use redirect to make sure a get request is generated
                '''
                if symb and quant:
                    print("BUYING")

                    date = d.datetime.now()
                    date = date.strftime("%m/%d/%Y, %H:%M:%S")

                    quant = int(quant)
                    print("AMOUNT", quant)
                    stock_price = getdata(close='close', symbol=symb)[0]
                    print("STOCK PRICE", stock_price)

                    total = quant * stock_price

                    print("You have spent $", total)

                    print("USER EMAIL:", user_email)
                    stock.buy("stock", (date, symb, stock_price, quant, user_email[0]), path)

                    data = (symb, stock_price, quant, total, user_email[0], date)
                    send_buy(data)

                    print("TRANSACTIONS: ", transactions)
                    # Redirect submits a get request (200) thus cancelling the usual post request generated by the
                    # browser when a page is refreshed
                    return redirect(url_for("trade"))

                # If the user hasnt filled in both the fields then he is redirected back to that page instead of the
                # program throwing an error
                else:
                    print("Field Empty")
                    return redirect(url_for("trade"))


            # SELLING
            elif request.form.get("s1"):
                # The data from the fields on the page are fetched
                symb = request.form["stockid"]
                quant = request.form["amount"]

                '''
                If both the fields had data then the quantity is stored as an integer
                The stock price api is called to calculate the price of that particular stock
                The total amount of money received is then calculated using price and quantity
                The STOCK TABLE is then updated with this data using the sell function
                A mail is sent to the user alerting them of the transaction made
                The user is now redirected back to the trade page - we use redirect to make sure a get request is generated
                '''
                if symb and quant:
                    print("SELLING")
                    print("DELETING SYMBOL:", symb)

                    quant = int(quant)
                    print("AMOUNT", quant)
                    stock_price = getdata(close='close', symbol=symb)[0]
                    print("STOCK PRICE", stock_price)

                    total = quant * stock_price
                    print("You have received $", total)

                    date = d.datetime.now()
                    date = date.strftime("%m/%d/%Y, %H:%M:%S")

                    data = (symb, quant, user_email[0])
                    stock.sell("stock", data, path)

                    mail_data = (symb, stock_price, quant, total, user_email[0], date)
                    send_sell(mail_data)
                    return redirect(url_for("trade"))

                # If the user hasnt filled in both the fields then he is redirected back to that page instead of the
                # program throwing an error
                else:
                    print("Field Empty")
                    return redirect(url_for("trade"))


            # FIND PRICE
            elif request.form.get("p1"):
                # The data from the fields on the page are fetched
                sym = request.form["stockid"]
                quant = request.form["amount"]

                '''
                If the user wants to find the price of a stock they can enter the symbol they want to find the price for
                and the amount
                The API fetches the price and then returns the value
                The user is then given the price of that stock for the amount they entered
                '''
                if sym and quant:
                    print("PRICE")
                    quant = int(quant)
                    print("AMOUNT", quant)

                    price = getdata(close='close', symbol=sym)[0]
                    price = float(price)

                    total = quant * price
                    print("Total cost is $", total)

                    quant = str(quant)
                    price = str(price)
                    total = str(total)

                    # Message with price for amount entered and per unit as well
                    err_str = "The price for " + quant + " unit(s) of " + sym + " Stock is $ " + total + " at $ " + price + " per unit"

                    print(transactions)
                    # render template because we want the table to show and the message
                    return render_template('trade.html', transactions=transactions, error=err_str)

                # If the user hasnt filled in both the fields then he is redirected back to that page instead of the
                # program throwing an error
                else:
                    print("Field Empty")
                    return redirect(url_for("trade"))

        return render_template('trade.html', transactions=transactions)
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect('/')


# CONTACT US page
@app.route('/contact', methods=["GET", "POST"])
def contact():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        
        """
        If a post request is generated (when user clicks submit)
        The email and message are fetched from the input fields
        The entered email is then checked with the database to make sure it matches the user and the user exists
        If the emails dont match it generates an error and if it does match then we insert data into contact table
        """
        if request.method == "POST":
            print("Contact Us")
            email = request.form["email"]
            print(email)
            msg = request.form["message"]

            user_email = g.user
            curr_user = user_email[0]
            print(curr_user)

            if users.check_contact_us(email, curr_user):
                print("Correct Email")
                contactus.insert(email, msg, path)
                return render_template('contact.html', error="Thank you, We will get back to you shortly")
            else:
                print("Incorrect Email")
                return render_template('contact.html', error="Incorrect Email!")

        return render_template("contact.html")

    # Redirects to login page if g.user is empty -> No user signed in
    return redirect('/')


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    with open('analysis/data/AAPL.json') as f:
        r = json.load(f)

    return {"res": r}


if __name__ == '__main__':
    app.run(debug=True, port=8000)