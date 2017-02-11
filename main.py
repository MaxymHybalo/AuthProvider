from provider.oauth2 import app
from provider.database import init_db

if __name__ == '__main__':
    init_db()
    app.secret_key = 'development'
    app.debug = True
    app.run(port=5001)
