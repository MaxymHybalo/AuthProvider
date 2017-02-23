from flask import Flask, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth


CLIENT_ID = 'FAg2xBX5D8ntUrcb9vf6sekXs7TR0rbrBqTdaX8V'
CLIENT_SECRET = 'fbRT8iGliufu8R279JghF96Angt4mMYWrSQOLttTwPhR7W074W'


app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
oauth = OAuth(app)

remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://18768e9c.ngrok.io/api/',
    request_token_url=None,
    access_token_url='http://18768e9c.ngrok.io/oauth/token',
    authorize_url='http://18768e9c.ngrok.io/oauth/authorize'
    # authorize_url='http://mendelson.ml/sobaken'
)
#
# Content-Type: application/x-www-form-urlencoded
# Content-Length: 149
#
# client_id=FAg2xBX5D8ntUrcb9vf6sekXs7TR0rbrBqTdaX8V&scope=email&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauthorized&confirm=yes


@app.route('/')
def index():
    if 'remote_oauth' in session:
        resp = remote.get('me')
        return jsonify(resp.data)
    next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    print(resp)
    session['remote_oauth'] = (resp['access_token'], '')
    return jsonify(oauth_token=resp['access_token'])


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')


if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(port=8000)
