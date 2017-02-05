from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from provider.models.user import User
from provider.database import db_session, init_db


app = Flask(__name__)
CORS(app)


@app.route("/auth/", methods=['POST'])
def authenticate():
    from provider.models.user import generate_access_token
    login = request.json.get('username')
    password = request.json.get('password')
    token = generate_access_token(login, password)
    return jsonify({'access_token': token})


@app.route("/user/", methods=['POST'])
def index():
    if request.method == 'POST':
        return str(signup_user(request.form))  # update method which work with json data form
    return make_response("Pass", 200)


@app.route("/test/api/", methods=['GET'])
def test():
    return jsonify({"submited": "all work's fine!"})


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
    app.run(port=5001)

