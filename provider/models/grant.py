from sqlalchemy import Column, String, Integer, \
    ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from provider.utils.database import Base, db_session

class Grant(Base):

    __tablename__ = 'grants'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User')
    client_id = Column(String(40), ForeignKey('clients.client_id'))
    client = relationship('Client')
    code = Column(String(255), index=True, nullable=False)
    redirect_uri = Column(String(255))
    expires = Column(DateTime)
    _scopes = Column(Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        return self
1