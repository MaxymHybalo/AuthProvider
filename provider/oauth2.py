from flask_oauthlib.provider import OAuth2Provider
from _datetime import datetime, timedelta
from flask import jsonify, request, render_template,session
from provider.routes_api import app
from provider.models.client import Client
from provider.models.grant import Grant
from provider.models.token import Token
from provider.models.user import User
from provider.database import db_session, init_db
from provider.jwt_auth import token_expected

oauth = OAuth2Provider(app)


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter(Client.client_id==client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter(Grant.client_id==client_id, Grant.code==code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=120)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=session_user(),  # TODO set current user,
        expires=expires
    )
    db_session.add(grant)
    db_session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter(Token.access_token == access_token).first()
    elif refresh_token:
        return Token.query.filter(Token.refresh_token == refresh_token).first()


@oauth.tokensetter
def save_token(token, req, *args, **kwargs):
    print(req)
    toks = Token.query.filter(Token.client_id == req.client.client_id and
                              Token.user_id == req.user.id)
    for t in toks:
        db_session.delete(t)
    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=req.client.client_id,
        user_id=req.user.id
    )

    db_session.add(tok)
    db_session.commit()
    return tok


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_handler():
    return None


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args,**kwargs):
    user = session_user()
    if not user:
        print('User did\'nt loaded')
        return jsonify({'message': False})
    if request.method == 'GET':
        client_id = kwargs['client_id']
        client = Client.query.filter(Client.client_id==client_id).first()
        kwargs['client'] = client
        print(user.to_string())
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)
    confirm = request.form.get('confirm', 'no')
    print("Confirm %s", confirm)
    return confirm == 'yes'


@app.route('/api/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.login)


@app.route('/client')
def client():
    user = current_user()
    if not user:
        return jsonify(message=False)
    item = Client(
        client_id='test_id',
        client_secret='test_secret',  # code by get_salt
        _redirect_uris=' '.join([
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized'
        ]),
        _default_scopes='email',
        user_id=user.id
    )
    init_db()
    db_session.add(item)
    db_session.commit()
    return jsonify(client_id=item.client_id, client_secret=item.client_secret)


def session_user():
    print('In session user call')
    return User.query.get(1)


@token_expected
def current_user(*args, **kwargs):
    if kwargs['verified']:
        print('OAuth.authorize_handler try to load User')
        return User.query.filter(User.login==kwargs['login']).first()
    return None





