from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text
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

    def to_string(self):
        return "{" \
               "\n\tid: " + str(self.id) + \
               "\n\tlogin: " + self.login +\
               "\n\tpassword: " + self.password +\
               "\n\tfirst_name: " + self.first_name +\
               "\n\tlast_name: " + self.last_name +\
               "\n\temail: " + self.email +\
               "\n\tphone: " + self.phone +\
               "\n}"  # to simplify user data output


class Client(Base):

    __tablename__ = 'clients'
    # Readable client name
    name = Column(String(30))

    description = Column(String(300))

    user_id = Column(ForeignKey('user.id'))
    user = relationship('User')
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), unique=True,
                           nullable=False,
                           index=True)
    is_confidential = Column(Boolean)
    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

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
        return self.redirect_uris[0];

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []



