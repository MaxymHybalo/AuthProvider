from flask import Blueprint, jsonify, request, abort, render_template, session
from provider.models.user import User, signup_user, user_information, update_user
from provider.utils.jwt_auth import generate_access_token
from datetime import datetime, timedelta
from provider.oauth2 import oauth

user_api = Blueprint('routes_api', __name__)


@user_api.route("/signup/", methods=['POST'])
def signup():
    response_message = signup_user(request.json)
    return jsonify({'message': response_message})


@user_api.route("/auth/", methods=['POST'])
def authenticate():
    token = generate_access_token(request.json)
    session['token'] = token
    print('Setted session: ', session['token'])
    session[token] = datetime.utcnow() + timedelta(days=1)
    return jsonify({'access_token': token})


@user_api.route('/api/profile/', methods=['GET', 'PUT'])
def profile():
    response_message = str(request.url) + " Success"
    if request.method == 'PUT':
        response_message = update_user(request.json)
        return jsonify(message=response_message)
    return user_information()


@user_api.route("/test/api/", methods=['GET'])
def test():
    return render_template('index.html')


def get_user_from_session():
    print(session['token'])
    from provider.utils.jwt_auth import session_user
    print('Pre-import call')
    print('Called get_user_from_session with')
    print(session['token'])
    return session_user(session['token'], session[session['token']])





