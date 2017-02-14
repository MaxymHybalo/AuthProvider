from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from provider.utils.database import Base, db_session
from provider.models.user import User
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


@token_expected
def add_client(json, **kwargs):
    user = None
    if kwargs['verified']:
        user = User.query.filter(User.login == kwargs['login']).first()
    if user:
        return write_to_database(json, user)
    return 'You are not authorized'


