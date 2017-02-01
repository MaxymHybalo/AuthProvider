from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from provider.database import Base

class Token(Base):

    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    client_id = Column(String(40), ForeignKey('clients.client_id'))
    client = relationship('Client')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    token_type = Column(String(40))  # Only bearer support
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires = Column(DateTime)
    _scopes = Column(Text)
    # TODO implement delete method


    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []