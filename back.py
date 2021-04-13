from flask import (
    Flask,
    session,
    g,
    render_template,
    request,
    redirect
)


import datetime as d
import os


#Imports functions from other folders
from models import users, contactus, stock
from sendmail import send_mail
from api import getdata


#Path used for all tables
path = "app.db"


templates_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=templates_path)
app.secret_key = 'somekey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


#Creates all the tables when the website is run
users.create_user()
contactus.create_tbl("app.db")
stock.make_tbl("app.db")


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


#Decorator for LOGIN page
@app.route('/', methods=["GET", "POST"])
def home():
    session.pop("user_email", None)
    flag = True
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        repeat_password = request.form['rpassword']

        if password:
            if len(repeat_password) == 0:
                print("Login")
                if users.checkpwd(password, email):
                    session['user_email'] = email
                    return redirect('/index')
                else:
                    flag=False

        if password and repeat_password:
            print("Sign In")
            if password == repeat_password:
                users.insert('user', (email, name, password, 0))
                session['user_email'] = email
                return render_template('login.html', error="Sign Up Complete - Login")
            else:
                return render_template('login.html', error="Password & Retyped Password Not Same")

        if not name and not password and email:
            if users.check_reset(email):
                print("Reset Password:")
                #session['user_email'] = email
                reset_password(email)
                return render_template('login.html', error="We have sent you a link to reset your password. Check your mailbox")
            else:
                print("User Doesnt Exist")
                return render_template('login.html', error="This Email Doesnt Exist - Please Sign Up")

    if flag:
        return render_template('login.html')
    else:
        return render_template('login.html', error="Incorrect Password")


#Decorator for HOME page
@app.route('/index')
def index():
    if g.user:
        return render_template('index.html')
    return redirect('/')



def reset_password(email : str):
    print(email)
    send_mail(email)


#Decorator for RESET PASSWORD page
@app.route('/reset', methods=["GET", "POST"])
def reset():
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
                    users.reset_pwd(pwd, ver_code)
                    print("Resetting password & Updating DB")
                    users.reset_code(ver_code)
                    return redirect("/")
                    #return render_template('login.html', error="Password Reset Successfully")
                else:
                    print("Verification Code Doesnt Match")
                    return redirect("/")
                    #return render_template('login.html', error="Try resetting again")
            else:
                return render_template('reset.html', error="Password & Retyped Password Not Same")
    return render_template('reset.html')


#Decorator for ANALYSIS page
@app.route('/inv')
def inv():
    if g.user:
        return render_template('inv.html')
    return redirect('/')


#Decorator for ABOUT US page
@app.route('/about')
def about():
    if g.user:
        return render_template('about.html')
    return redirect('/')


#Decorator for TRADE page
@app.route('/trade', methods=["GET", "POST"])
def trade():
    print(g.user)
    if g.user:
        user_email = g.user
        transactions = stock.query(user_email[0], path)

        if request.method == "POST":

            if request.form.get("b1"):
                print("BUYING")

                date = d.datetime.now()
                date = date.strftime("%m/%d/%Y, %H:%M:%S")

                symb = request.form["stockid"]

                quant = request.form["amount"]
                quant = int(quant)
                print("AMOUNT", quant)
                stock_price = getdata(close='close', symbol=symb)[0]
                print("STOCK PRICE", stock_price)

                total = quant * stock_price

                print("You have spent $", total)

                print("USER EMAIL:", user_email)
                stock.buy("stock", (date, symb, stock_price, quant, user_email[0]), path)

                
                print("TRANSACTIONS: ", transactions)

                return render_template('trade.html', transactions=transactions, error="Bought Successfully!")

            elif request.form.get("s1"):
                print("SELLING")

                symb = request.form["stockid"]
                print("DELETING SYMBOL:", symb)

                quant = request.form["amount"]
                quant = int(quant)
                print("AMOUNT", quant)
                stock_price = getdata(close='close', symbol=symb)[0]
                print("STOCK PRICE", stock_price)

                total = quant * stock_price
                print("You have received $", total)

                data = (symb, quant, user_email[0])
                stock.sell("stock", data, path)
                return render_template('trade.html', transactions=transactions, error="Sold Successfully!")

        return render_template('trade.html')

    return redirect('/')


#Decorator for CONTACT US page
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if g.user:
        if request.method == "POST":
            print("Contact Us")
            email = request.form["email"]
            print(email)
            msg = request.form["message"]
            user_email = users.getemail().pop()
            print(user_email[0])
            if email != user_email[0]:
                print("Incorrect Email")
                return render_template('contact.html', error="Incorrect Email!")
            print("Correct Email")
            contactus.insert(email, msg, path)
            return render_template('contact.html', error="Thank you, We will get back to you shortly")

        return render_template('contact.html')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
