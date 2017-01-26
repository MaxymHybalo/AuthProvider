from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import declarative_base



db = SQLAlchemy()
# Base = declarative_base()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True,
                         nullable=False)
    # first_name = db.Column(db.String(40),)

    def to_string(self):
        return "{" \
               "\n\tid: " + str(self.id) + \
               "\n\tlogin: " + self.username + \
               "\n}"  # to simplify user data output





