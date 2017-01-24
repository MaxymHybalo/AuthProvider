from flask import Flask
from flask import render_template
from flask import request
from provider.entities import User
from provider.entities import db


app = Flask(__name__)

@app.route("/signup/", methods = ['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        return request.form['login']
    return render_template("index.html")


if __name__ == '__main__':

    app.debug = True
    app.secret_key = 'development'
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///users.db'
    })
    db.init_app(app)
    db.app = app
    db.create_all()

    # user = User(username='esd1th')
    # try:
    #     db.session.add(user)
    #     db.session.commit()
    # except:
    #     db.session.rollback()

    print(User.query.get(2).username)
    app.run()
