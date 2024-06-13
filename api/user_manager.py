from flask import Flask, request, jsonify, abort, Blueprint
from model.user import User
from persistence.DataManager import DataManager

user_manager_blueprint = Blueprint('user_manager', __name__)
data_manager = DataManager()


@user_manager_blueprint.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400, description="Missing required fields")

    email = request.json['email']
    password = request.json['password']
    first_name = request.json.get('first_name', '')
    last_name = request.json.get('last_name', '')

    if '@' not in email:
        abort(400, description="Invalid email format")

    existing_users = [user for user in data_manager.storage.get(
        'User', {}).values() if user.email == email]
    if existing_users:
        abort(409, description="Email already exists")

    user = User(email=email, password=password,
                first_name=first_name, last_name=last_name)
    data_manager.save(user)

    return jsonify(user.to_dict()), 201


@user_manager_blueprint.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict()
             for user in data_manager.storage.get('User', {}).values()]
    return jsonify(users), 200


@user_manager_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user is None:
        abort(404, description="User not found")
    return jsonify(user.to_dict()), 200


@user_manager_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user is None:
        abort(404, description="User not found")

    if not request.json:
        abort(400, description="Missing required fields")

    user.email = request.json.get('email', user.email)
    user.password = request.json.get('password', user.password)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)

    data_manager.update(user)
    return jsonify(user.to_dict()), 200


@user_manager_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user is None:
        abort(404, description="User not found")
    data_manager.delete(user_id, 'User')
    return '', 204