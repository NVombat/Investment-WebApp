from flask import (
    Flask, 
    session, 
    g,
    render_template
)
import os 

templates_path = os.path.abspath('./templates')
app = Flask(__name__, template_folder=templates_path)

@app.before_request
def execute():
    print("entered something")

@app.route('/')
def login():

    # TODO 

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