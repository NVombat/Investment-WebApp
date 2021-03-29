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
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)