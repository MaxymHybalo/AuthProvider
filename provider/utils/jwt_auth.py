from flask import request, session

import jwt


def token_expected(f):
    def wrapper(*args, **kwargs):
        data = dict()
        data['verified'] = False
        if request.headers.get('Authorization'):
            token = request.headers['Authorization'].split(' ')
            data = _get_token_data(token)
            print(data)
        if data['verified']:
            return f(*args, verified=data['verified'], login=data['login'])
        return f(*args, verified=data['verified'])
    return wrapper


def _get_token_data(token):
    data = dict()
    if token:
        try:
            data = jwt.decode(token[1], 'key', algorithms=['HS256'])
        except jwt.InvalidTokenError:
            data['verified'] = False
    return data


def generate_access_token(json):
    from provider.models.user import User
    user = None
    if 'login' and 'password' in json:
        user = User.query.filter(User.login == json['login']).first()
    if user and user.check_password(json['password']):
        token = jwt.encode({'login': json['login'], 'verified': True}, key='key', algorithm='HS256')
        print('Returned ', token.decode('utf-8'))
        return token.decode('utf-8')
    token = jwt.encode({'login': json['login'], 'verified': False}, key='key', algorithm='HS256')
    return token.decode('utf-8')


def session_user(header):
    from provider.models.user import User
    from datetime import datetime
    print('Callded session_user')
    print(_get_token_data(header))
    login = _get_token_data(header)['login']
    return User.query.filter(User.login == login).first()

