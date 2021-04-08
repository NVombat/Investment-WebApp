from flask import (
    Flask,
    session,
    g,
    render_template,
    request,
    redirect
)

import datetime as d
from models import users, contactus, stock
from api import getdata
import os

#Path used for all tables
path = "app.db"

templates_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=templates_path)
app.secret_key = 'somekey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

users.create_user()
contactus.create_tbl("app.db")
stock.make_tbl("app.db")


@app.before_request
def security():
    g.user = None
    for i in session:
        print(session[i])
    if 'user_email' in session:
        emails = getemail()
        try:
            useremail = [email for email in emails if email[0] == session['user_email']][0]
            g.user = useremail
        except Exception as e:
            print("Failed")


@app.route('/', methods=["GET", "POST"])
def home():
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
                    return render_template('index.html')
                else:
                    flag=False

        if password and repeat_password:
            print("Sign In")
            if password == repeat_password:
                users.insert('user', (email, name, password))
                #session['user_email'] = email
                return render_template('login.html')
            else:
                return render_template('login.html', error="Password & Retyped Password Not Same")
        if not name:
            print("Reset Password")
    if flag:
        return render_template('login.html')
    else:
        return render_template('login.html', error="Incorrect Password")
    
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/inv')
def inv():
    return render_template('inv.html')

def transact(data : tuple):
    transactions = []
    for d in data:
        transactions.append(d)



@app.route('/trade', methods=["GET", "POST"])
def trade():
    if request.method == "POST":

        if request.form.get("b1"):
            print("BUYING")
            date = d.datetime.now()
            date = date.strftime("%m/%d/%Y, %H:%M:%S")

            symb = request.form["stockid"]

            quant = request.form["amount"]

            quant = int(quant)
            print("AMOUNT", quant)
            total = getdata(close='close', symbol=symb)[0]

            total = quant * total

            user_email = users.getemail().pop()
            user_email = user_email[0]
            print("USER EMAIL:", user_email)
            stock.buy("stock", (date, symb, total, quant, user_email), path)

            #For the table
            transactions = []
            data = (date, symb, total, quant, user_email,)
            for ele in data:
                transactions.append(ele)
            return render_template('trade.html', transactions=transactions, error="Bought Successfully!")
        
        elif request.form.get("s1"):
            print("SELLING")
            symb = request.form["stockid"]
            print("DELETING SYMBOL:", symb)
            quant = request.form["amount"]
            quant = int(quant)
            print("AMOUNT", quant)
            stock.sell("stock", symb, quant, path)
            return render_template('trade.html', error="Sold Successfully!")



    return render_template('trade.html')

#print(stock.query("ronaldo72emiway@gmail.com", "app.db"))

@app.route('/contact', methods=["GET", "POST"])
def contact():
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

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if request.method()=="POST":
        session.pop()
        g.user = None
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
