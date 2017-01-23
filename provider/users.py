from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:////home/sashok/users.bd', convert_unicode=True, echo=True)
Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    login = Column(String)
    password = Column(String)
    email = Column(String)
    phone_number = Column(Integer)


    def __init__(self, first_name, last_name, login, password, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password = password
        self.email = email
        self.phone_number


Base.metadata.create_all(engine)


u = User('Rusya', 'Sadboy', 'login', 'password', 'email', '12373897')
db_session.add(u)
db_session.commit()