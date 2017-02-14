from flask import Blueprint, jsonify, request, abort, render_template

from provider.models.user import User, signup_user, user_information
from provider.utils.jwt_auth import token_expected

user_api = Blueprint('routes_api', __name__)


@user_api.route("/signup/", methods=['POST'])
def signup():
    response_message = signup_user(request.json)
    return jsonify({'message': response_message})


@user_api.route("/auth/", methods=['POST'])
def authenticate():
    from provider.models.user import generate_access_token
    token = generate_access_token(request.json)
    return jsonify({'access_token': token})


# @user_api.route('/api/user/<changable_field>')

@user_api.route('/api/profile/', methods=['GET'])
def profile():
    return user_information()


@user_api.route("/test/api/", methods=['GET'])
def test():
    return render_template('index.html')


@user_api.route("/showusers", methods=['GET'])
def all_users():
    # @token_expected
    def foo(*args, **kwargs):
        users = User.query.all()
        all_users = ''
        print('[Logger] Show users method entered')
        for u in users:
            all_users += u.to_string() + "\n"
        return all_users
    return foo()







