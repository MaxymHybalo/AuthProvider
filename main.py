from provider.oauth2 import app

if __name__ == '__main__':
    app.secret_key = 'development'
    app.debug = True
    app.run(port=5001)
