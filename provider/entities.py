from sqlalchemy import Column, String, Integer
from provider.database import Base


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(40), unique=True, index=True,
                         nullable=False)

    first_name = Column(String(40), nullable=False)

    def to_string(self):
        return "{" \
               "\n\tid: " + str(self.id) + \
               "\n\tlogin: " + self.login +\
               "\n\tfirst_name: " + self.first_name +\
               "\n}"  # to simplify user data output





