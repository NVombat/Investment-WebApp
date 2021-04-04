from flask import (
    Flask,
    session,
    g,
    render_template,
    request,
    redirect
)

from models import users, contact

import os

templates_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=templates_path)
app.secret_key = 'somekey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

users.create_user()
contact.create_tbl("app.db")


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
            print("failed")


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
                print("login")
                if users.checkpwd(password, email):
                    return render_template('index.html')
                else:
                    flag=False

        if password and repeat_password:
            print("sign in")
            if password == repeat_password:
                users.insert('user', (email, name, password))
                return render_template('login.html')
            else:
                return render_template('login.html', error="Password and Retyped Password not same")
        if not name:
            print("Reset Password")
    if flag:
        return render_template('login.html')
    else:
        return render_template('login.html', error="Incorrect Password")
    

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    # if request.method == "POST":
    #     #TODO


    return render_template('contact.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/inv')
def inv():
    return render_template('inv.html')


@app.route('/trade')
def trade():
    return render_template('trade.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
