from flask import Blueprint, jsonify, request, redirect, render_template, session, make_response, Response
from werkzeug.exceptions import abort
from provider.models.user import (User, signup_user, user_information, update_user,
                                   current_session_user, token_user)

from provider.utils.jwt_auth import generate_access_token
from provider.routes.service_routes import check_for_error, clear_session

user_api = Blueprint('routes_api', __name__)


@user_api.route('/')
def home():
    return render_template('index.html', user=current_session_user())


@user_api.route("/signup/", methods=['POST'])
def signup():
    response_message = signup_user(request.json)
    return check_for_error(response_message)


@user_api.route("/auth/", methods=['POST'])
def authenticate():
    token, error = generate_access_token(request.json)
    if error:
        return abort(make_response(jsonify(error=error), 503))
    token_id = token_user(token)
    if token_id:
        clear_session()
        print('[LOG] Session call in /auth')
        session['id'] = token_id
    return jsonify({'access_token': token})


@user_api.route('/api/profile/', methods=['GET', 'PUT'])
def profile():
    if request.method == 'PUT':
        response_message = update_user(request.json)
        return check_for_error(response_message)
    return user_information()
