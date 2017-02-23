from flask import Blueprint, jsonify, request, redirect, render_template, session

from provider.models.user import User, signup_user, user_information, update_user, current_session_user
from provider.utils.jwt_auth import generate_access_token


user_api = Blueprint('routes_api', __name__)


@user_api.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        clear_session()
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter(User.login == login).first()
        if user and user.check_password(password):
            session['id'] = user.id
        return redirect('/')
    return render_template('login.html')


@user_api.route('/logout', methods=['POST'])
def logout():
    clear_session()
    return redirect('/')


@user_api.route('/')
def home():
    return render_template('index.html', user=current_session_user())


@user_api.route("/signup/", methods=['POST'])
def signup():
    response_message = signup_user(request.json)
    return jsonify({'message': response_message})


@user_api.route("/auth/", methods=['POST'])
def authenticate():
    token = generate_access_token(request.json)
    return jsonify({'access_token': token})


@user_api.route('/api/profile/', methods=['GET', 'PUT'])
def profile():
    if request.method == 'PUT':
        response_message = update_user(request.json)
        return jsonify(message=response_message)
    return user_information()


def clear_session():
    if 'id' in session:
        session.pop('id')


