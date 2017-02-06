from sqlalchemy import Column, String, Integer
from provider.database import Base
from flask import request
from provider.database import init_db, db_session


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True, index=True,
                   nullable=False)
    password = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(40), nullable=False)
    phone = Column(String(20))

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


def signup_user(json):
    if json:
        init_db()
        if User.query.filter(User.login == json['username']).first():
            return False
        username = json['username']
        password = json['password']
        email = json['email']
        phone = json['phone']
        first_name = json['firstName']
        last_name = json['lastName']
        user = User(login=username, password=password, email=email, phone=phone,
                    first_name=first_name, last_name=last_name)
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
    # TODO Handle exception
    except:
        db_session.rollback()
    if user and user.check_password(password):
        token = jwt.encode({'login': login, 'verified': True}, key='key', algorithm='HS256')
        return token.decode('utf-8')
    token = jwt.encode({'login': login, 'verified': False}, key='key', algorithm='HS256')
    return token.decode('utf-8')


