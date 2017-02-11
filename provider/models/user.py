from sqlalchemy import Column, String, Integer
from provider.database import init_db, db_session, Base
from provider.jwt_auth import token_expected
import re


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True, index=True,
                   nullable=False)
    password = Column(String(400), nullable=False)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    email = Column(String(40), nullable=False)
    phone = Column(String(20))

    # TODO bad json data
    def __init__(self, json):
        if json:
            self.login = json['login']
            self.password = json['password']
            self.email = json['email']
            self.phone = json['phone']
            self.first_name = json['firstName']
            self.last_name = json['lastName']

    def check_password(self, password):
        from passlib.hash import pbkdf2_sha256
        return pbkdf2_sha256.verify(password, self.password)

    def to_string(self):
        return "{" \
               "\n\tid: " + str(self.id) + \
               "\n\tlogin: " + self.login + \
               "\n\tpassword: " + self.password + \
               "\n\tfirst_name: " + self.first_name + \
               "\n\tlast_name: " + self.last_name + \
               "\n\temail: " + self.email + \
               "\n\tphone: " + self.phone + \
               "\n}"  # For simplify user data output


def encrypt_password(password):
    from passlib.hash import pbkdf2_sha256
    hashed = pbkdf2_sha256.hash(password)
    return hashed


def signup_user(user):

    if User.query.filter(User.login == user.login).first():
        return False
    try:
        user.password = encrypt_password(user.password)
        db_session.add(user)
        print("User added to session")
        db_session.commit()
        print("[New user ", user.login, "]")
    except:
        print("[error catch]")
        db_session.rollback()
    return True


def generate_access_token(json):
    import jwt
    user = None
    if 'login' and 'password' in json:
        user = User.query.filter(User.login == json['login']).first()
    if user and user.check_password(json['password']):
        token = jwt.encode({'login': json['login'], 'verified': True}, key='key', algorithm='HS256')
        return token.decode('utf-8')
    token = jwt.encode({'login': json['login'], 'verified': False}, key='key', algorithm='HS256')
    return token.decode('utf-8')


@token_expected
def user_information(**kwargs):
    from flask import jsonify
    response = jsonify({"message": False})
    if kwargs['verified']:
        try:
            user = User.query.filter(User.login == kwargs['login']).first()
            response = jsonify({
                    'login': user.login,
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'phone': user.phone,
                    'email': user.email
                })
        except:
            db_session.remove()
        return response


def test_user_select():
    u = User.query.get(1)
    u.first_name
    return u.first_name
