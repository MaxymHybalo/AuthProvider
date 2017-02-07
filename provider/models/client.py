from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from provider.database import Base


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
