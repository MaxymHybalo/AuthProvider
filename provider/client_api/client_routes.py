from flask import Blueprint, jsonify, request
from provider.models.user import User
from provider.models.client import Client, add_client
from provider.utils.database import db_session

client_routes = Blueprint('client_routes', __name__)


@client_routes.route('/client/', methods=['POST'])
def client():
    return jsonify(message=add_client(request.json))

# @client_routes.route('/client')
# def client():
#     user = session_user()
#     if not user:
#         return jsonify(message="You are not authorized")
#     item = Client(
#         client_id='test_id',
#         client_secret='test_secret',  # code by get_salt
#         _redirect_uris=' '.join([
#             'http://localhost:8000/authorized',
#             'http://127.0.0.1:8000/authorized',
#             'http://dc63510e.ngrok.io/authorized'
#         ]),
#         _default_scopes='email',
#         user_id=user.id
#     )
#
#     db_session.add(item)
#     db_session.commit()
#     return jsonify(client_id=item.client_id, client_secret=item.client_secret)
