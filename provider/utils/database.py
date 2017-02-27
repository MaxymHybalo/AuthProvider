from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

mysql_url_localbase = 'mysql+cymysql://root:root@127.0.0.1:3306/auth_provider_dev'

mysql_deploy = 'mysql+cymysql://b5115c396daeef:4c7e36b8@us-cdbr-iron-east-04.cleardb.net/heroku_33d6128a0e767a7'

sqlite_url = 'sqlite:////dev.db'


engine = create_engine(mysql_deploy, encoding='utf-8')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    engine.execute('SET NAMES utf8')
    engine.execute('SET character_set_connection=utf8;')
    import provider.models
    Base.metadata.create_all(bind=engine)