from datetime import datetime, timedelta
from flask import Flask
from flask_cors import CORS
from provider.utils.database import init_db, db_session

app = Flask(__name__, template_folder='templates')


def setup():
    from provider.oauth2 import oauth
    app.debug = True
    app.secret_key = 'secret'
    CORS(app)
    setup_blueprints()
    oauth.init_app(app)
    init_db()


def setup_blueprints():
    from provider.user_api.user_routes import user_api
    from provider.client_api.client_routes import client_routes
    from provider.oauth2 import oauth_api
    app.register_blueprint(user_api)
    app.register_blueprint(client_routes)
    app.register_blueprint(oauth_api)


# TODO Deploying config, change db location
#
setup()
#
# Local development server config
#
if __name__ == '__main__':
    setup()
    app.run()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



