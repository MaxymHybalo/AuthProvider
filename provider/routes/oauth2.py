from datetime import datetime, timedelta
from flask_oauthlib.provider import OAuth2Provider
from flask import Blueprint, redirect, request, render_template, jsonify, make_response, url_for
from provider.models.client import Client
from provider.models.grant import Grant
from provider.models.token import Token
from provider.models.user import User, current_session_user
from provider.utils.database import db_session
from sqlalchemy.exc import InvalidRequestError


oauth_api = Blueprint('oauth_api', __name__)
oauth = OAuth2Provider()


@oauth.clientgetter
def load_client(client_id):
    client = None
    try:
        client = Client.query.filter_by(client_id=client_id).first()
    except InvalidRequestError:
        db_session.remove()
    return client


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_session_user(),
        expires=expires
    )
    db_session.add(grant)
    db_session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
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
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db_session.add(tok)
    db_session.commit()
    return tok


@oauth_api.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@oauth_api.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    client_id = kwargs.get('client_id')
    client = Client.query.filter_by(client_id=client_id).first()
    user = current_session_user()
    print(request)
    if not user:
        return redirect(url_for('routes_api.login_redirect', returnUrl=client.redirect_uris[0]))
    if request.method == 'GET':
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@oauth_api.route('/api/me')
@oauth.require_oauth()
def me():

    user = request.oauth.user
    return jsonify(username=user.login, email=user.email)

