from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates
from sqlalchemy.exc import SQLAlchemyError
from provider.utils.database import db_session, Base
from provider.utils.jwt_auth import token_expected
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

    def __init__(self, json):
        if json:
            self.login = json['login']
            self.password = json['password']
            self.email = json['email']
            self.phone = json['phone']
            self.first_name = json['firstName']
            self.last_name = json['lastName']

    @validates('email')
    def validate_login(self, key, email):
        assert '@' in email
        return email

    @validates('login')
    def validate_login(self,login):
        pattern = ''.join(re.findall(r'\w\n', login))

    def check_password(self, password):
        from passlib.hash import pbkdf2_sha256
        return pbkdf2_sha256.verify(password, self.password)

    def assign_updates(self, json):
        if 'firstName' in json:
            self.first_name = json['firstName']
        if 'lastName' in json:
            self.last_name = json['lastName']
        if 'email' in json:
            self.email = json['email']
        if 'phone' in json:
            self.phone = json['phone']

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


def signup_user(json):
    if json:
        try:
            user = User(json)
            submitted = write_user_to_db(user)
            if submitted:
                return 'User register success'
        except KeyError:
            return 'Wrong request data'
        except AssertionError:
            return 'User data invalid'
    return 'Some server error'


def encrypt_password(password):
    from passlib.hash import pbkdf2_sha256
    hashed = pbkdf2_sha256.hash(password)
    return hashed


def write_user_to_db(user):
    if User.query.filter(User.login == user.login).first():
        return False
    try:
        user.password = encrypt_password(user.password)
        db_session.add(user)
        print("User added to session")
        db_session.commit()
        print("[New user ", user.login, "]")
    except SQL:
        print("[error catch]")
        db_session.rollback()
    return True


def update_user(json):
    user = current_user()
    user.assign_updates(json)
    try:
        db_session.commit()
    except SQLAlchemyError:
        return 'Server error'
    print('[Logger] user inf. wrote to db')
    return 'Change user information accepted'


def user_information():
    from flask import jsonify
    response = jsonify({"message": False})
    try:
        user = current_user()
        response = jsonify({
                    'login': user.login,
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'phone': user.phone,
                    'email': user.email
                })
    except SQLAlchemyError:
        db_session.remove()
    return response


@token_expected
def current_user(**kwargs):
    if kwargs['verified']:
        return User.query.filter(User.login == kwargs['login']).first()
