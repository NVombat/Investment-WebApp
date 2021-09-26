# Imports
from flask import render_template, redirect, request, session, url_for, Flask, g

from dotenv import load_dotenv
from requests.api import get
from pathlib import Path
import yfinance as yf
import datetime as d
import pynance as pn
import pandas as pd
import requests
import binascii
import glob
import json
import time
import os
import io

from sendmail import send_mail, send_buy, send_sell
from models import users, contactus, stock
from api import getdata


# Import environment variables
load_dotenv()
key_id = os.getenv("KEY_ID")
key_secret = os.getenv("KEY_SECRET")


# Initialize Payment Session
request_payment = requests.Session()
request_payment.auth = (key_id, key_secret)
payment_data = json.load(open("payment_data.json"))
# print("Payment Data:", payment_data)


# Path used for all tables in database
path = "app.db"


# To pass data from one page to another
class state:
    ...


s = state()


# App configuration
templates_path = os.path.abspath("./templates")
app = Flask(__name__, template_folder=templates_path)
app.secret_key = "somekey"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


# Creates all the tables in the database when the application is run
users.create_user(path)
contactus.create_tbl(path)
stock.make_tbl(path)


def get_current_price(symbol: str) -> float:
    """Gets current closing price of any stock using Ticker method

    Args:
        symbol: Stock Symbol

    Returns:
        float: Closing Stock price
    """
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return todays_data["Close"][0]


def get_current_stock_price(symbol: str) -> float:
    """Gets current closing price of any stock
    (Substitute for init function error)

    Args:
        symbol: Stock Symbol

    Returns:
        float: Closing Stock price
    """
    data = pn.data.get(symbol, start=None, end=None)
    return data["Close"][0]


# API Class for currency conversion
class Currency_Conversion:
    # Store the conversion rates
    rates = {}

    def __init__(self, url):
        data = requests.get(url).json()
        # Extracting only the rates from the json data
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount) -> float:
        """Converts one currency to another

        Args:
            from_currency: Currency to be converted from
            to_cuurency: Currency to be converted to
            amount: amount to be converted

        Returns:
            float: Converted amount
        """
        initial_amount = amount
        if from_currency != "EUR":
            amount = amount / self.rates[from_currency]

        amount = round(amount * self.rates[to_currency], 2)
        return amount


"""
List of stock symbols to see if the user has entered a valid stock symbol
URL containing NASDAQ listings in csv format
"""
url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
data = requests.get(url).content
df_data = pd.read_csv(io.StringIO(data.decode("utf-8")))
symbols = df_data["Symbol"].to_list()


@app.before_request
def security():
    """
    Sets the current user - g.user to none and checks if the user is in session
    If user is in session then their email is fetched and g.user is updated to that email
    """
    g.user = None
    if "user_email" in session:
        emails = users.getemail(path)
        try:
            useremail = [
                email for email in emails if email[0] == session["user_email"]
            ][0]
            g.user = useremail
        except Exception as e:
            print("Failed")


# LOGIN page
@app.route("/", methods=["GET", "POST"])
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
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        repeat_password = request.form["rpassword"]

        if password and not repeat_password:
            """
            LOGIN -> Check if user exists
            """
            if users.check_user_exist(path, email):
                """
                Check the password against the hashed password in the db
                If it matches, user is in session and is redirected to the homepage
                Else flag is set and the user is shown an error message
                """
                if users.check_hash(path, password, email):
                    session["user_email"] = email
                    return redirect("/index")
                else:
                    # User has entered the wrong password
                    flag = False
                    return render_template(
                        "login.html", error="Incorrect Email or Password"
                    )
            else:
                # User doesnt exist
                return render_template("login.html", error="User Doesnt Exist")

        """
        If the password and repeat password fields are filled - SIGN UP
        If the user already exists then print an error message and redirect to login page
        If the user doesnt exist then allow the signup to take place
        If they both are the same (password and repeat password)
        Then a new user is added to the USER TABLE in the database with all the data
        The user is then added to the session and the user is redirected to the login page
        If the fields dont match the user is alerted and redirected back to the login page to try again
        """
        if password and repeat_password:
            print("SIGN UP")
            if not users.check_user_exist(path, email):
                if password == repeat_password:
                    # Hash the users password and store the hashed password
                    password = users.hash_pwd(password)
                    # print("Hashed PWD: ", password)
                    users.insert(path, "user", (email, name, password, 0))
                    # print("Inserted Hashed Password")
                    session["user_email"] = email
                    return render_template(
                        "login.html", error="Sign Up Complete - Login"
                    )
                else:
                    return render_template(
                        "login.html", error="Password & Retyped Password Not Same"
                    )
            else:
                return render_template(
                    "login.html", error="This User Already Exists! Try Again"
                )

        """
        If only the email field is filled it means the user has requested to reset their password
        First the User table is looked up to see if the user exists (if the password can be reset)
        The password is reset if the user exists through the reset process (mail, verification code ...)
        If the user doesnt exist an error message is generated and the user is redirected back to the login page
        """
        if not name and not password and email:
            if users.check_user_exist(path, email):
                print("RESET PASSWORD:")
                # session['user_email'] = email
                reset_password(path, email)
                return render_template(
                    "login.html",
                    error="We have sent you a link to reset your password. Check your mailbox",
                )
            else:
                print("User Doesnt Exist")
                return render_template(
                    "login.html", error="This Email Doesnt Exist - Please Sign Up"
                )

    # If the flag variable is true then the user has entered the correct password and is redirected to the login page
    # FLAG VALUE IS TRUE INITIALLY
    if flag:
        return render_template("login.html")


# HOME page
@app.route("/index", methods=["GET", "POST"])
def index():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template("index.html")
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect("/")


def reset_password(path: str, email: str):
    """
    Reset password
    Sends the mail for resetting password to user
    """
    # print(email)
    send_mail(path, email)


# RESET PASSWORD page
@app.route("/reset", methods=["GET", "POST"])
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
        pwd = request.form["npassword"]
        repeat_pwd = request.form["rnpassword"]
        ver_code = request.form["vcode"]
        try:
            ver_code = int(ver_code)
        except:
            raise TypeError
        # print(ver_code)

        if pwd and repeat_pwd and ver_code:
            print("CHECKING")
            if pwd == repeat_pwd:
                if users.check_code(path, ver_code):
                    # Hash the new password and update db with hashed password
                    pwd = users.hash_pwd(pwd)
                    users.reset_pwd(path, pwd, ver_code)
                    # print("Resetting password & Updating DB")
                    users.reset_code(path, ver_code)
                    return redirect("/")
                    # return render_template('login.html', error="Password Reset Successfully")
                else:
                    # print("Verification Code Doesnt Match")
                    # return redirect("/")
                    return render_template(
                        "reset.html", error="Incorrect Verification Code"
                    )
            else:
                return render_template(
                    "reset.html", error="Password & Retyped Password Not Same"
                )
    return render_template("reset.html")


# ANALYSIS page -> Allows user to get historical stock data for any company and then view it graphically
@app.route("/inv", methods=["GET", "POST"])
def inv():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        # If the user clicks on the 'VIEW' Button a POST request is generated
        if request.method == "POST":
            # print("ENTERED POST REQUEST")
            # Get the variable name for the option the the user has entered
            stock_id = request.form["stocksym"]
            stock_id = stock_id.upper()
            # print(stock_id)

            # If the stock symbol is valid and exists
            if stock_id in symbols:
                # print(stock_id)
                # Fetch data into another dataframe
                df_stock = yf.download(stock_id, start="1950-01-01", period="1d")
                # print(df_stock)
            # If stock symbol is invalid
            else:
                # Return to page with error
                return render_template(
                    "inv.html",
                    error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                )

            # Drop the 'Adj Close' column as we dont need it to plot data
            df_stock.drop("Adj Close", axis="columns", inplace=True)

            # Reset index makes sure the dataframe has indexing of its own and converts the date index to a column
            df_stock.reset_index(inplace=True)

            # Convert the date to a datetime object (gets converted to a specialised type of datetime object)
            df_stock["Date"] = pd.to_datetime(df_stock["Date"])

            # Convert date to epoch datetime format
            df_stock["Date"] = (
                df_stock["Date"] - d.datetime(1970, 1, 1)
            ).dt.total_seconds()

            # Format for plotting requires specific size for date so multiply by 1000
            df_stock["Date"] = df_stock["Date"] * 1000
            # print(df_stock.head())

            # Gets a list of all files ending in _mod.json
            files = glob.glob(
                "/home/nvombat/Desktop/Investment-WebApp/analysis/data/*_mod.json"
            )
            # If there is such a file (list is not empty)
            if len(files) != 0:
                # Extract the file name of that particular file
                file_rem = Path(files[0]).name
                # print("FILE BEING DELETED IS:", file_rem)
                # Get the path of that file
                location = "/home/nvombat/Desktop/Investment-WebApp/analysis/data/"
                path = os.path.join(location, file_rem)
                # Delete the file
                os.remove(path)

            # We delete the file to make sure that at any given time there is only one file that can be plotted
            # As the plotting function chooses the first file from the directory (files[0])
            # Thus if we have more than one file we may not end up plotting the correct data

            # Convert to json format and make sure its converted as json with arrays thus orient = values
            df_stock.to_json(
                "/home/nvombat/Desktop/Investment-WebApp/analysis/data/"
                + stock_id
                + "_mod.json",
                orient="values",
            )
            # return redirect(url_for("inv"))
            return render_template("inv.html", name=stock_id)

        return render_template("inv.html")
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect("/")


# ABOUT US page
@app.route("/about")
def about():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template("about.html")
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect("/")


# TRADING GUIDE page
@app.route("/doc")
def doc():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:
        return render_template("doc.html")
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect("/")


# TRADE page
@app.route("/trade", methods=["GET", "POST"])
def trade():
    # Enters the page only if a user is signed in - g.user represents the current user
    # print("G.USER:", g.user)
    if g.user:

        """
        uses the user email id to query the users transactions
        this transactions array is then received by the table on the html page
        """
        user_email = g.user
        transactions = stock.query(user_email[0], path)
        # print("TRANSACTIONS: ", transactions)

        if request.method == "POST":

            # To convert Dollars to Rupees
            url = str.__add__(
                "http://data.fixer.io/api/latest?access_key=",
                os.getenv("CURRENCY_ACCESS_KEY"),
            )
            c = Currency_Conversion(url)
            from_country = "USD"
            to_country = "INR"
            # c.convert(from_country, to_country, amount)

            """
            If a post request is generated (button clicked) the user wants to buy or sell stocks
            It is then checked whether the user wants to buy or sell (based on the button pressed)
            """
            # BUYING
            if request.form.get("b1"):
                # The data from the fields on the page are fetched
                symb = request.form["stockid"]
                quant = request.form["amount"]

                """
                The stock symbol entered is capitalised as all symbols are always capitalized
                The stock symbol is checked for validity
                Then the current date and time is calculated
                Then the quantity is stored as an integer
                The stock price api/stock price function is called to calculate the price of that particular stock
                The total amount of money spent is then calculated using price and quantity
                The format of price and total is adjusted to 2 decimal places
                The STOCK TABLE is then updated with this data using the buy function
                A mail is sent to the user alerting them of the transaction made
                The user is now redirected back to the trade page - we use redirect to make sure a get request is generated
                """
                print("BUYING")
                symb = symb.upper()
                # Check if the stock symbol is valid
                if symb in symbols:
                    date = d.datetime.now()
                    date = date.strftime("%m/%d/%Y, %H:%M:%S")

                    quant = int(quant)
                    # print("AMOUNT", quant)

                    # stock_price = getdata(close='close', symbol=symb)[0]
                    # stock_price = get_current_price(symb)
                    stock_price = get_current_stock_price(symb)
                    # print("STOCK PRICE", stock_price)
                    total = quant * stock_price

                    stock_price = "{:.2f}".format(stock_price)
                    total = "{:.2f}".format(total)
                    # print("You have spent $", total)

                    stock_price_float = float(stock_price)
                    stock_price_rupees = c.convert(
                        from_country, to_country, stock_price_float
                    )
                    stock_price_int = int(stock_price_rupees)
                    stock_price_int *= 100
                    # print("INT VAL OF STOCK PRICE: ", stock_price_int)

                    # ref_id = binascii.b2a_hex(os.urandom(20))
                    # # print(ref_id.decode())
                    # payment_data["amount"] = stock_price_int
                    # payment_data["reference_id"] = ref_id.decode()
                    # payment_data["customer"]["name"] = users.getname(path, g.user)
                    # payment_data["customer"]["email"] = user_email[0]

                    # # print("PAYMENT DATA AFTER UPDATE:", payment_data)

                    # payment_link_init = request_payment.post(
                    #     "https://api.razorpay.com/v1/payment_links/",
                    #     headers={"Content-Type": "application/json"},
                    #     data=json.dumps(payment_data),
                    # ).json()
                    # # print(payment_link_init)
                    # payment_link = payment_link_init["short_url"]

                    # return redirect(payment_link, code=303)

                    # print("USER EMAIL:", user_email)
                    stock.buy(
                        "stock", (date, symb, stock_price, quant, user_email[0]), path
                    )

                    data = (symb, stock_price, quant, total, user_email[0], date)
                    send_buy(path, data)

                    # print("TRANSACTIONS: ", transactions)
                    # Redirect submits a get request (200) thus cancelling the usual post request generated by the
                    # browser when a page is refreshed
                    return redirect(url_for("trade"))
                # If stock symbol is invalid
                else:
                    # Return to page with error
                    return render_template(
                        "trade.html",
                        error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                        transactions=transactions,
                    )

            # SELLING
            elif request.form.get("s1"):
                # The data from the fields on the page are fetched
                symb = request.form["stockid"]
                quant = request.form["amount"]

                """
                The stock symbol entered is capitalised as all symbols are always capitalized
                The stock symbol is checked for validity
                Then the quantity is stored as an integer
                The stock price api/stock price function is called to calculate the price of that particular stock
                The total amount of money received is then calculated using price and quantity
                The format of price and total is adjusted to 2 decimal places
                The STOCK TABLE is then updated with this data using the sell function
                A mail is sent to the user alerting them of the transaction made
                The user is now redirected back to the trade page - we use redirect to make sure a get request is generated
                """
                symb = symb.upper()
                if symb in symbols:
                    print("SELLING")
                    # print("DELETING SYMBOL:", symb)

                    quant = int(quant)
                    # print("AMOUNT", quant)

                    # stock_price = getdata(close='close', symbol=symb)[0]
                    # stock_price = get_current_price(symb)
                    stock_price = get_current_stock_price(symb)
                    # print("STOCK PRICE", stock_price)

                    # stock_price_rupees = c.convert(from_country, to_country, stock_price)
                    # print("CONVERTED AMOUNT: ", stock_price_rupees)

                    total = quant * stock_price
                    # print("You have received $", total)

                    stock_price = "{:.2f}".format(stock_price)
                    total = "{:.2f}".format(total)

                    date = d.datetime.now()
                    date = date.strftime("%m/%d/%Y, %H:%M:%S")
                    # print(type(date))

                    data = (symb, quant, user_email[0], stock_price)

                    if(stock.sell("stock", data, path)):
                        mail_data = (symb, stock_price, quant, total, user_email[0], date)
                        send_sell(path, mail_data)
                        return redirect(url_for("trade"))
                    else:
                        return render_template(
                        "trade.html",
                        error="You either DO NOT own this stock or are trying to sell more than you own! Please check again!",
                        transactions=transactions,
                    )

                # If stock symbol is invalid
                else:
                    return render_template(
                        "trade.html",
                        error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                        transactions=transactions,
                    )

            # FIND PRICE
            elif request.form.get("p1"):
                # The data from the fields on the page are fetched
                sym = request.form["stockid"]
                quant = request.form["amount"]

                """
                If the user wants to find the price of a stock they can enter the symbol they want to find the price for
                and the amount
                The stock symbol entered is capitalised as all symbols are always capitalized
                The API/Function fetches the price and then returns the value
                The format of price and total is adjusted to 2 decimal places
                The user is then given the price of that stock for the amount they entered
                """
                sym = sym.upper()
                # First we check if the stock symbol is valid
                if sym in symbols:
                    print("PRICE")

                    quant = int(quant)
                    # print("AMOUNT", quant)

                    # price = getdata(close='close', symbol=sym)[0]
                    # price = get_current_price(sym)
                    price = get_current_stock_price(sym)
                    # print("PRICE:", price)
                    price = float(price)

                    total = quant * price
                    # print("Total cost is $", total)

                    # stock_price_rupees = c.convert(from_country, to_country, price)
                    # print("CONVERTED PRICE: ", stock_price_rupees)

                    price = "{:.2f}".format(price)
                    total = "{:.2f}".format(total)

                    quant = str(quant)
                    price = str(price)
                    total = str(total)

                    # Message with price for amount entered and per unit as well
                    err_str = (
                        "The price for "
                        + quant
                        + " unit(s) of "
                        + sym
                        + " Stock is $ "
                        + total
                        + " at $ "
                        + price
                        + " per unit"
                    )

                    # print(transactions)
                    # render template because we want the table to show and the message
                    return render_template(
                        "trade.html", transactions=transactions, error=err_str
                    )
                # If stock symbol is invalid
                else:
                    return render_template(
                        "trade.html",
                        error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                        transactions=transactions,
                    )

        return render_template("trade.html", transactions=transactions)
    # Redirects to login page if g.user is empty -> No user signed in
    return redirect("/")


# CONTACT US page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    # Enters the page only if a user is signed in - g.user represents the current user
    if g.user:

        """
        If a post request is generated (when user clicks submit)
        The email and message are fetched from the input fields
        The entered email is then checked with the database to make sure it matches the user and the user exists
        If the emails dont match it generates an error and if it does match then we insert data into contact table
        Redirects to login page if g.user is empty -> No user signed in
        """
        if request.method == "POST":
            print("CONTACT US")
            email = request.form["email"]
            # print(email)
            msg = request.form["message"]

            user_email = g.user
            curr_user = user_email[0]
            # print(curr_user)

            if users.check_contact_us(path, email, curr_user):
                # print("Correct Email")
                contactus.insert(email, msg, path)
                return render_template(
                    "contact.html", error="Thank you, We will get back to you shortly"
                )
            else:
                # print("Incorrect Email")
                return render_template("contact.html", error="Incorrect Email!")

        return render_template("contact.html")
    return redirect("/")


@app.route("/pipe", methods=["GET", "POST"])
def pipe():
    """
    Function sends data (in json format) to the plotting function
    Gets a list of all files in the data folder which have a _mod.json ending
    If there are no such files then plot AAPL as the default graph
    If there is such a file - sends json file containing data to be plotted
    """
    files = glob.glob(
        "/home/nvombat/Desktop/Investment-WebApp/analysis/data/*_mod.json"
    )
    if len(files) == 0:
        with open(
            "/home/nvombat/Desktop/Investment-WebApp/analysis/data/AAPL.json"
        ) as f:
            r = json.load(f)
            return {"res": r}
    else:
        with open(files[0]) as f:
            r = json.load(f)
            return {"res": r}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
