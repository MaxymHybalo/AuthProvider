from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from provider.models.user import signup_user
from provider.database import db_session
from provider.jwt_auth import token_expected
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
CORS(app)


@app.route("/user/", methods=['POST'])
def index():
    if request.method == 'POST':
        return str(signup_user(request.form))  # TODO update method which work with json data form
    return make_response("Pass", 200)


@app.route("/auth/", methods=['POST'])
def authenticate():
    from provider.models.user import generate_access_token
    # TODO check data existing
    login = request.json.get('username')
    password = request.json.get('password')
    token = generate_access_token(login, password)
    return jsonify({'access_token': token})


@app.route("/test/api/", methods=['GET'])
def test():
    # TODO seems like needed to carry out routes logic to another function
    @token_expected
    def func(*args, **kwargs):
        print(kwargs)
        if kwargs['verified']:
            return jsonify({"submited": "all work's fine!"})
        return jsonify({"denied": "authorization error"})
    return func()


@app.route("/showusers", methods=['GET'])
def all_users():
    @token_expected
    def foo(*args, **kwargs):
        init_db()
        users = User.query.all()
        all_users = ''
        for u in users:
            all_users += u.to_string() + "\n"
        return all_users
    return foo()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'development'
    app.run(port=5001)

