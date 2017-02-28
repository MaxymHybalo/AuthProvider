from flask import request, session

import jwt
from provider.utils.database import db_session
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session


def token_expected(f):
    def wrapper(*args, **kwargs):
        data = dict()
        data['verified'] = False
        if request.headers.get('Authorization'):
            token = request.headers['Authorization'].split(' ')
            data = _get_token_data(token[1])
            print(data)
        if data['verified']:
            return f(*args, verified=data['verified'], login=data['login'])
        return f(*args, verified=data['verified'])
    return wrapper


def _get_token_data(token):
    data = dict()
    if token:
        try:
            data = jwt.decode(token, 'key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            data['verified'] = False
        except jwt.InvalidTokenError:
            data['verified'] = False
    return data


def generate_access_token(json):
    from provider.models.user import User
    user = None
    if 'login' and 'password' in json:
        try:
            user = User.query.filter(User.login == json['login']).first()
        except OperationalError:
            db_session.close()
            return None, 'Databasse error handling'
    if user and user.check_password(json['password']):
        from datetime import datetime, timedelta
        token = jwt.encode({'login': json['login'],
                            'verified': True,
                            'exp': datetime.utcnow() + timedelta(days=1)},
                           key='key', algorithm='HS256')

        return token.decode('utf-8'), None
    token = jwt.encode({'login': json['login'], 'verified': False}, key='key', algorithm='HS256')
    return token.decode('utf-8'), 'Bad user credentials'


def session_user(header):
    from provider.models.user import User
    from datetime import datetime
    print('Callded session_user')
    print(_get_token_data(header))
    login = _get_token_data(header)['login']
    return User.query.filter(User.login == login).first()

