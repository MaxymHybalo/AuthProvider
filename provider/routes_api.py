from flask import Flask, render_template, make_response, jsonify
from provider.entities import User
from provider.database import db_session, init_db
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route("/user/", methods=['POST'])
def index():
    if request.method == 'POST':
        return str(signup_user(request.form))  # update method which work with json data form
    return make_response("Pass", 200)


@app.route("/test/api/", methods=['GET'])
@auth.login_required
def test():
    return jsonify({"submited": "all work's fine!"})


@auth.get_password
def get_password(login):
    init_db()
    user = User.query.filter(User.login == login).first()
    if user:
        return user.password
    return None


@auth.error_handler
def auth_error():
    return make_response(jsonify({'error': 'Unauthorized error'}))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def signup_user(form):
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
    app.run()

