from flask import request
import jwt


def token_expected(f):
    def wrapper(*args, **kwargs):
        # TODO change to getting token from header
        token = request.json.get('access_token')
        print(token)
        if token:
            data = jwt.decode(token, 'key', algorithms=['HS256'])
            if data['verified']:
                print('Readed as bool')
                # TODO *args **kwargs
            return f(*args, **kwargs)
    return wrapper

