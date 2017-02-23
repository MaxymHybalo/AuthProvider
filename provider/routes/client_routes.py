from flask import Blueprint, jsonify, request
from provider.models.user import User
from provider.models.client import Client, add_client, get_user_clients, delete_client
from provider.utils.database import db_session

client_routes = Blueprint('client_routes', __name__)


@client_routes.route('/client/', methods=['POST', 'GET'])
def client():
    if request.method == 'POST':
        print('[LOG] Client creating')
        return jsonify(message=add_client(request.json))
    result = get_user_clients()
    print('[LOG] Client fetching')
    if isinstance(result, list):
        return jsonify(result)
    return jsonify(error=result)


@client_routes.route('/client/<string:client_id>/', methods=['DELETE'])
def del_client(client_id):
    result = delete_client(client_id)
    if result[0]:
        return jsonify(message=result[1])
    return jsonify(error=result[1])


