from flask import Blueprint, jsonify, request, redirect, render_template, session, make_response

service_api = Blueprint('service_api', __name__)


@service_api.route('/login')
def login_redirect():
    return render_template('index.html')


@service_api.route('/register')
def register_redirect():
    return render_template('index.html')


@service_api.route('/profile')
def profile_redirect():
    return render_template('index.html')


@service_api.route('/logout', methods=['POST'])
def logout():
    clear_session()
    return redirect('/')


def clear_session():
    print('[LOG] Clear session call')
    if 'id' in session:
        session.pop('id')


def check_for_error(message, code=503):
    if 'error' in message:
        return abort(make_response(jsonify(message), code))
    return jsonify(message)
