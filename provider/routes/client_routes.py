from flask import Blueprint, jsonify, request
from provider.models.user import User
from provider.models.client import Client, add_client, get_user_clients, delete_client
from provider.utils.database import db_session
from provider.routes.service_routes import check_for_error

client_routes = Blueprint('client_routes', __name__)


@client_routes.route('/client/', methods=['POST', 'GET'])
def client():
    if request.method == 'POST':
        print('[LOG] Client creating')
        message = add_client(request.json)
        return check_for_error(message)
    result = get_user_clients()
    print('[LOG] Client fetching')
    if isinstance(result, list):
        return jsonify(result)
    return check_for_error(result)


@client_routes.route('/client/<string:client_id>/', methods=['DELETE'])
def del_client(client_id):
    result = delete_client(client_id)
    return check_for_error(result)
