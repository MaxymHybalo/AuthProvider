from flask import request
import jwt


def token_expected(f):
    def foo(*args, **kwargs):
        data = dict()
        data['verified'] = False
        if request.headers.get('Authorization'):
            token = request.headers['Authorization'].split(' ')
            data = get_token_data(token)
        if data['verified']:
            return f(*args, verified=data['verified'], login=data['login'])
        return f(*args, verified=data['verified'])
    return foo


def get_token_data(token):
    data = dict()
    if token:
        try:
            data = jwt.decode(token[1], 'key', algorithms=['HS256'])
        except jwt.InvalidTokenError:
            data['verified'] = False
    return data
