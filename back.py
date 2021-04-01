from flask import (
    Flask, 
    session, 
    g,
    render_template,
    request,
    redirect
)

from models.users import (
    checkpwd,
    create_user, 
    insert,
    getname,
    getemail
)

from models.contact import (
    create_tbl,
    insert
)

import os 

app = Flask(__name__)
app.secret_key = 'somekey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

create_user()
create_tbl("app.db")

templates_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=templates_path)

@app.before_request
def execute():
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

@app.route('/', methods=['GET', 'POST'])
def login():
    print("IN LOGIN")
    session.pop("user_email", None)
    if request.method == "POST":
        email = request.form["email"]
        try:
            name = request.form['name']
        except Exception as e:
            name = None


        password = request.form['password']

        if name != None:

            insert("user", values=(email, name, password))
            session['user_email'] = email
            return redirect('upload')
       
        if name == None:
            if checkpwd(password, email):
               
                session['user_email'] = email ## session makes a cookie
                return redirect('index.html')
        return redirect("/")

    return render_template('login.html')

@app.route('/about.html')
def about():

    return render_template('about.html')

@app.route('/contact.html')
def contact():

    return render_template('contact.html')

@app.route('/index.html')
def index():

    return render_template('index.html')

@app.route('/inv.html')
def inv():

    return render_template('inv.html')

@app.route('/trade.html')
def trade():

    return render_template('trade.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)