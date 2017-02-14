from flask import Blueprint, jsonify, request
from provider.models.user import User
from provider.models.client import Client, add_client
from provider.utils.database import db_session

client_routes = Blueprint('client_routes', __name__)


@client_routes.route('/client/', methods=['POST'])
def client():
    return jsonify(message=add_client(request.json))
