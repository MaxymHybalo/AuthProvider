from flask import Flask, url_for, session, request, jsonify, render_template, redirect
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

)


@app.route('/')
def index():
    if 'remote_oauth' in session:
        resp = remote.get('me')
        return render_template('client.html', email=resp.data['email'], login=resp.data['username'])
    next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/profile', methods=['GET'])
def login():
    if 'remote_oauth' in session:
        resp = remote.get('me')
        return render_template('client.html', email=resp.data['email'], login=resp.data['username'])
    return render_template('client.html')


@app.route('/login/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    print(resp)
    session['remote_oauth'] = (resp['access_token'], '')
    # return jsonify(oauth_token=resp['access_token'])
    return redirect('/profile')


@app.route('/logout')
def logout():
    session.pop('remote_oauth')
    return redirect('/')


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')


if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(port=8000)
