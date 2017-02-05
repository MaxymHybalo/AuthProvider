from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from provider.database import Base


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

    def check_password(self,password):
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


def generate_access_token(login,password):
    from provider.database import init_db
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
        return str(token)
    token = jwt.encode({'login': login, 'verified': False}, key='key', algorithm='HS256')
    return str(token)
