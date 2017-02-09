from sqlalchemy import Column, String, Integer
from provider.database import init_db, db_session, Base
from provider.jwt_auth import token_expected
import re


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True, index=True,
                   nullable=False)
    password = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(40), nullable=False)
    phone = Column(String(20))
    # TODO bad json data

    def __init__(self, json):
        if json:
            self.login = json['username']
            self.password = json['password']
            self.email = json['email']
            self.phone = json['phone']
            self.first_name = json['firstName']
            self.last_name = json['lastName']

    def check_password(self, password):
        if password and self.password == password:
            return True
        return False

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


#Todo Verification

def verify_by_pattern(value, reg_exp, error_message=None):
    for char in value:
        if not re.findall(reg_exp, char):
            return False, error_message
    return True, None
# for first, last name pattern r'[a-zA-Zа-яА-Я]'

def encrypting_pass(password):
    from passlib.context import CryptContext
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])
    hash_pass = myctx.hash(password)
    return hash_pass
# method decryption password pbkdf2_sha256.verify(password, hash)

def signup_user(user):
    if User.query.filter(User.login == user.login).first():
        return False
    try:
        db_session.add(user)
        db_session.commit()
    except:
        db_session.rollback()
    return True


def generate_access_token(login, password):
    import jwt
    user = None
    try:
        init_db()
        user = User.query.filter(User.login == login).first()
    except:
        db_session.rollback()
    if user and user.check_password(password):
        token = jwt.encode({'login': login, 'verified': True}, key='key', algorithm='HS256')
        return token.decode('utf-8')
    token = jwt.encode({'login': login, 'verified': False}, key='key', algorithm='HS256')
    return token.decode('utf-8')


@token_expected
def user_information(**kwargs):
    from flask import jsonify
    response = jsonify({"message": False})
    if kwargs['verified']:
        try:
            user = User.query.filter(User.login == kwargs['login']).first()
            response = jsonify({
                    'username': user.login,
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'phone': user.phone,
                    'email': user.email
                })
        except:
            db_session.remove()
        return response
