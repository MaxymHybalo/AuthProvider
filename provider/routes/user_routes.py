from flask import Blueprint, jsonify, request, redirect, render_template, session

from provider.models.user import User, signup_user, user_information, update_user
from provider.utils.jwt_auth import generate_access_token

user_api = Blueprint('routes_api', __name__)


@user_api.route('/login', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        session.pop('id')
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter(User.login == login).first()
        if user and user.check_password(password):
            session['id'] = user.id
        return redirect('/login')
    from provider.models.user import current_session_user
    return render_template('home.html', user=current_session_user())


@user_api.route('/logout', methods=['POST'])
def logout():
    session.pop('id')
    return redirect('/')


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
    response_message = str(request.url) + " Success"
    if request.method == 'PUT':
        response_message = update_user(request.json)
        return jsonify(message=response_message)
    return user_information()


def get_user_from_session():
    print(session['token'])
    from provider.utils.jwt_auth import session_user
    print('Pre-import call')
    print('Called get_user_from_session with')
    print(session['token'])
    return session_user(session['token'], session[session['token']])





