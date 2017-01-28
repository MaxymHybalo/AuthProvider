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
        return str(signin_user(request.form))
    return render_template("index.html")


@app.route("/showusers", methods=['GET'])
def all_users():
    init_db()
    users = User.query.all()
    all_users = ''
    for u in users:
        all_users += u.to_string() + "\n"
    return all_users


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def signin_user(form):
    if form:
        init_db()
        if User.query.filter(User.login == form['login']).first():
            return False
        user = User(login=form['login'],
                    password=form['password'],
                    first_name=form['first'],
                    last_name=form['last'],
                    email=form['email'],
                    phone=form['number'])
        try:
            db_session.add(user)
            db_session.commit()
        except:
            db_session.rollback()
        return True


if __name__ == '__main__':

    app.debug = True
    app.secret_key = 'development'
    init_db()
    # Hot to write to database
    # try:
    #     u = User(login="another", first_name="Max")
    #     db_session.add(u)
    #     db_session.commit()
    #     print("Writed")
    # except:
    #     db_session.rollback()
    app.run()

