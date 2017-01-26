from flask import Flask
from flask import render_template
from flask import request
from provider.entities import User
from provider.database import db_session, init_db


app = Flask(__name__)


@app.route("/signup/", methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':

        return request.form['login']
    return render_template("index.html")


@app.route("/showusers", methods=['GET'])
def all_users():
    users = User.query.all()
    all_users = ''
    for u in users:
        all_users += u.to_string() + "\n"
    return all_users


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':

    app.debug = True
    app.secret_key = 'development'
    init_db()
    app.run()
    # try:
    #     u = User(login="sS", first_name="Sd")
    #     db_session.add(u)
    #     db_session.commit()
    # except:
    #     db_session.rollback() method to write into database