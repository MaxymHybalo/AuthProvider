from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from provider.utils.database import Base, db_session
from provider.models.user import User, current_user
from provider.models.token import Token
from provider.utils.jwt_auth import token_expected
from werkzeug.security import gen_salt


class Client(Base):

    __tablename__ = 'clients'
    # Readable client name
    name = Column(String(30))
    description = Column(String(300))
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User')
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), unique=True,
                           nullable=False,
                           index=True)
    is_confidential = Column(Boolean)
    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

    def __init__(self, json):
        self.name = json['name']
        self.description = json['description']
        self._redirect_uris = json['url']

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.client_id,
            'secret': self.client_secret
        }

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


def write_to_database(json, user):
    try:
        client = Client(json)
    except KeyError:
        return 'Wrong request data'
    try:
        client.client_id = gen_salt(40)
        client.client_secret = gen_salt(50)
        client._default_scopes = 'email'
        client.user_id = user.id
        db_session.add(client)
        db_session.commit()
    except SQLAlchemyError:
        return 'Database writing error'
    return 'Client added success'


def add_client(json):
    user = current_user()
    if user:
        return write_to_database(json, user)
    return 'You are not authorized'


def delete_client(id):
    user = current_user()
    if user:
        client = Client.query.filter(Client.client_id == id).first()
        if client.user_id == user.id:
            result = _delete_cascade(client)
            if result:
                return True, 'Client successful deleted'
    return False, 'Delete operation error, user or client id wrong'


def _delete_cascade(client):
    try:
        _delete_client_tokens(client)
        db_session.delete(client)
        db_session.commit()
    except SQLAlchemyError:
        return False
    return True


def _delete_client_tokens(client):
    try:
        tokens = Token.query.filter(Token.client_id == client.client_id).all()
        for t in tokens:
            db_session.delete(t)
        db_session.commit()
    except SQLAlchemyError:
        pass


def get_user_clients():
    user = current_user()
    if user:
        clients = Client.query.filter(Client.user == user).all()
        dilist = list()
        for i in clients:
            dilist.append(i.serialize())
        return dilist
    return "Something work falsely"
