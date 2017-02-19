from flask import Blueprint, jsonify, request
from provider.models.user import User
from provider.models.client import Client, add_client, get_user_clients
from provider.utils.database import db_session

client_routes = Blueprint('client_routes', __name__)


@client_routes.route('/client/', methods=['POST', 'GET'])
def client():
    if request.method == 'POST':
        result = add_client(request.json)
        return jsonify(message=result)
    result = get_user_clients()
    if isinstance(result, list):
        return jsonify(result)
    return jsonify(error=result)
