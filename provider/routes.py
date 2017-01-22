from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/signup/", methods = ['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        return request.form['login']
    return render_template("index.html")

