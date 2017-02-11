from flask import Flask, make_response, jsonify, request, session
from flask_cors import CORS
from provider.models.user import signup_user, User, user_information
from provider.database import db_session, init_db
from provider.jwt_auth import token_expected


app = Flask(__name__)
CORS(app)


@app.route("/signup/", methods=['POST'])
def signup():
    if request.json:
        user = User(request.json)
        submitted = signup_user(user)
        if submitted:
            return jsonify({"message": True})
    return jsonify({'message': False})


@app.route("/auth/", methods=['POST'])
def authenticate():
    from provider.models.user import generate_access_token
    token = generate_access_token(request.json)
    return jsonify({'access_token': token})


@app.route('/api/profile/', methods=['GET'])
def profile():
    return user_information()


@app.route("/test/api/", methods=['GET'])
def test():
    # TODO seems like needed to carry out routes logic to another function
    @token_expected
    def func(*args, **kwargs):
        print(kwargs)
        if kwargs['verified']:
            return jsonify({"submitted": "all work's fine!"})
        return jsonify({"denied": "authorization error"})
    from provider.models.user import test_user_select
    return test_user_select()


@app.route("/showusers", methods=['GET'])
def all_users():
    # @token_expected
    def foo(*args, **kwargs):
        init_db()
        users = User.query.all()
        all_users = ''
        for u in users:
            all_users += u.to_string() + "\n"
        return all_users
    return foo()


def session_user():
    return User.query.get(1)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


