from flask import Flask
from flask_cors import CORS

from provider.utils.database import init_db

app = Flask(__name__)
CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    from provider.utils.database import db_session
    db_session.remove()


def setup_blueprints():
    from provider.user_api.user_routes import user_api
    from provider.client_api.client_routes import client_routes
    from provider.oauth2 import oauth_routes
    app.register_blueprint(user_api)
    app.register_blueprint(client_routes)
    app.register_blueprint(oauth_routes)

if __name__ == '__main__':
    init_db()
    app.secret_key = 'development'
    app.debug = True
    setup_blueprints()
    app.run()
