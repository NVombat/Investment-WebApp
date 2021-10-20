# Imports
from flask import render_template, redirect, request, session, url_for, Flask, g
from dotenv import load_dotenv
from pathlib import Path
import yfinance as yf
import datetime as d
import pynance as pn
import pandas as pd
import requests
import glob
import json
import os
import io

from sendmail import send_mail, send_buy, send_sell
from models import users, contactus, stock

# Import environment variables
load_dotenv()
key_id = os.getenv("KEY_ID")
key_secret = os.getenv("KEY_SECRET")


# Initialize Payment Session
request_payment = requests.Session()
request_payment.auth = (key_id, key_secret)
payment_data = json.load(open("payment_data.json"))


# Path to database
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


# Create tables
users.create_user(path)
contactus.create_tbl(path)
stock.make_tbl(path)


def get_current_price(symbol: str) -> float:
    """Gets current closing price of stock using Ticker method

    Args:
        symbol: Stock Symbol

    Returns:
        float: Closing Stock price
    """
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return float(todays_data["Close"][0])


def get_current_stock_price(symbol: str) -> float:
    """Gets current closing price of stock
    (Substitute for init function error)

    Args:
        symbol: Stock Symbol

    Returns:
        float: Closing Stock price
    """
    data = pn.data.get(symbol, start=None, end=None)
    return float(data["Close"][0])


class Currency_Conversion:
    """
    API Class for currency conversion
    """
    rates = {}

    def __init__(self, url):
        data = requests.get(url).json()
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



# List of stock symbols from URL containing NASDAQ listings
url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
data = requests.get(url).content
df_data = pd.read_csv(io.StringIO(data.decode("utf-8")))
symbols = df_data["Symbol"].to_list()


@app.before_request
def security():
    """
    Sets current user (g.user) to none and checks if the user is in session
    If in session then email is fetched and g.user is updated to that email
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


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Login Page
    """
    session.pop("user_email", None)

    flag = True

    # Store input if a post request is made
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        repeat_password = request.form["rpassword"]

        if password and not repeat_password:
            if users.check_user_exist(path, email):
                if users.check_hash(path, password, email):
                    session["user_email"] = email
                    return redirect("/index")
                else:
                    flag = False
                    return render_template(
                        "login.html", error="Incorrect Email or Password"
                    )
            else:
                return render_template("login.html", error="User Doesnt Exist")

        if password and repeat_password:
            if not users.check_user_exist(path, email):
                if password == repeat_password:
                    password = users.hash_pwd(password)
                    users.insert(path, "user", (email, name, password, 0))
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

        if not name and not password and email:
            if users.check_user_exist(path, email):
                reset_password(path, email)
                return render_template(
                    "login.html",
                    error="We have sent you a link to reset your password. Check your mailbox",
                )
            else:
                return render_template(
                    "login.html", error="This Email Doesnt Exist - Please Sign Up"
                )

    if flag:
        return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    """
    Home Page
    """
    if g.user:
        return render_template("index.html")
    return redirect("/")


def reset_password(path: str, email: str):
    """
    Sends mail for resetting password to user
    """
    send_mail(path, email)


@app.route("/reset", methods=["GET", "POST"])
def reset():
    """
    Reset Password Page
    """
    if request.method == "POST":
        pwd = request.form["npassword"]
        repeat_pwd = request.form["rnpassword"]
        ver_code = request.form["vcode"]
        try:
            ver_code = int(ver_code)
        except:
            raise TypeError

        if pwd and repeat_pwd and ver_code:
            if pwd == repeat_pwd:
                if users.check_code(path, ver_code):
                    pwd = users.hash_pwd(pwd)
                    users.reset_pwd(path, pwd, ver_code)
                    users.reset_code(path, ver_code)
                    return redirect("/")
                else:
                    return render_template(
                        "reset.html", error="Incorrect Verification Code"
                    )
            else:
                return render_template(
                    "reset.html", error="Password & Retyped Password Not Same"
                )
    return render_template("reset.html")


@app.route("/inv", methods=["GET", "POST"])
def inv():
    """
    Analysis Page - displays historical stock data
    """
    if g.user:
        if request.method == "POST":
            stock_id = request.form["stocksym"]
            stock_id = stock_id.upper()

            if stock_id in symbols:
                df_stock = yf.download(stock_id, start="1950-01-01", period="1d")

            else:
                return render_template(
                    "inv.html",
                    error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                )

            df_stock.drop("Adj Close", axis="columns", inplace=True)
            df_stock.reset_index(inplace=True)
            df_stock["Date"] = pd.to_datetime(df_stock["Date"])
            df_stock["Date"] = (
                df_stock["Date"] - d.datetime(1970, 1, 1)
            ).dt.total_seconds()
            df_stock["Date"] = df_stock["Date"] * 1000

            files = glob.glob(
                "/home/nvombat/Desktop/Investment-WebApp/analysis/data/*_mod.json"
            )

            if len(files) != 0:
                file_rem = Path(files[0]).name
                location = "/home/nvombat/Desktop/Investment-WebApp/analysis/data/"
                path = os.path.join(location, file_rem)
                os.remove(path)

            df_stock.to_json(
                "/home/nvombat/Desktop/Investment-WebApp/analysis/data/"
                + stock_id
                + "_mod.json",
                orient="values",
            )
            return render_template("inv.html", name=stock_id)

        return render_template("inv.html")
    return redirect("/")


@app.route("/about")
def about():
    """
    About Us Page
    """
    if g.user:
        return render_template("about.html")
    return redirect("/")


@app.route("/doc")
def doc():
    """
    Trading Guide Page
    """
    if g.user:
        return render_template("doc.html")
    return redirect("/")


@app.route("/trade", methods=["GET", "POST"])
def trade():
    """
    Trade Page - Buy, Sell & View the price of stocks
    """
    if g.user:
        user_email = g.user
        transactions = stock.query(user_email[0], path)

        if request.method == "POST":
            url = str.__add__(
                "http://data.fixer.io/api/latest?access_key=",
                os.getenv("CURRENCY_ACCESS_KEY"),
            )
            c = Currency_Conversion(url)
            from_country = "USD"
            to_country = "INR"

            # BUYING
            if request.form.get("b1"):
                symb = request.form["stockid"]
                quant = request.form["amount"]

                symb = symb.upper()
                if symb in symbols:
                    date = d.datetime.now()
                    date = date.strftime("%m/%d/%Y, %H:%M:%S")

                    quant = int(quant)
                    stock_price = get_current_stock_price(symb)
                    total = quant * stock_price

                    stock_price = "{:.2f}".format(stock_price)
                    total = "{:.2f}".format(total)

                    stock_price_rupees = c.convert(
                        from_country, to_country, stock_price
                    )
                    stock_price_int = int(stock_price_rupees)
                    stock_price_int *= 100

                    # ref_id = binascii.b2a_hex(os.urandom(20))
                    # payment_data["amount"] = stock_price_int
                    # payment_data["reference_id"] = ref_id.decode()
                    # payment_data["customer"]["name"] = users.getname(path, g.user)
                    # payment_data["customer"]["email"] = user_email[0]

                    # payment_link_init = request_payment.post(
                    #     "https://api.razorpay.com/v1/payment_links/",
                    #     headers={"Content-Type": "application/json"},
                    #     data=json.dumps(payment_data),
                    # ).json()
                    # payment_link = payment_link_init["short_url"]

                    # return redirect(payment_link, code=303)

                    stock.buy(
                        "stock", (date, symb, stock_price, quant, user_email[0]), path
                    )

                    data = (symb, stock_price, quant, total, user_email[0], date)
                    send_buy(path, data)

                    return redirect(url_for("trade"))

                else:
                    return render_template(
                        "trade.html",
                        error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                        transactions=transactions,
                    )

            # SELLING
            elif request.form.get("s1"):
                symb = request.form["stockid"]
                quant = request.form["amount"]
                symb = symb.upper()

                if symb in symbols:
                    quant = int(quant)
                    stock_price = get_current_stock_price(symb)
                    total = quant * stock_price
                    stock_price = "{:.2f}".format(stock_price)
                    total = "{:.2f}".format(total)

                    date = d.datetime.now()
                    date = date.strftime("%m/%d/%Y, %H:%M:%S")
                    data = (symb, quant, user_email[0], stock_price)

                    if stock.sell("stock", data, path):
                        mail_data = (
                            symb,
                            stock_price,
                            quant,
                            total,
                            user_email[0],
                            date,
                        )
                        send_sell(path, mail_data)
                        return redirect(url_for("trade"))

                    else:
                        return render_template(
                            "trade.html",
                            error="You either DO NOT own this stock or are trying to sell more than you own! Please check again!",
                            transactions=transactions,
                        )

                else:
                    return render_template(
                        "trade.html",
                        error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                        transactions=transactions,
                    )

            # FIND PRICE
            elif request.form.get("p1"):
                sym = request.form["stockid"]
                quant = request.form["amount"]
                sym = sym.upper()

                if sym in symbols:
                    quant = int(quant)
                    price = get_current_stock_price(sym)
                    price = float(price)

                    total = quant * price
                    price = "{:.2f}".format(price)
                    total = "{:.2f}".format(total)

                    quant = str(quant)
                    price = str(price)
                    total = str(total)

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

                    return render_template(
                        "trade.html", transactions=transactions, error=err_str
                    )

                else:
                    return render_template(
                        "trade.html",
                        error="Incorrect Stock Symbol. Please Enter Valid Symbol",
                        transactions=transactions,
                    )

        return render_template("trade.html", transactions=transactions)
    return redirect("/")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Contact Us Page
    """
    if g.user:
        if request.method == "POST":
            email = request.form["email"]
            msg = request.form["message"]

            user_email = g.user
            curr_user = user_email[0]

            if users.check_contact_us(path, email, curr_user):
                contactus.insert(email, msg, path)
                return render_template(
                    "contact.html", error="Thank you, We will get back to you shortly"
                )

            else:
                return render_template("contact.html", error="Incorrect Email!")

        return render_template("contact.html")
    return redirect("/")


@app.route("/pipe", methods=["GET", "POST"])
def pipe():
    """
    Analysis Substitute Page
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
