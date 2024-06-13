from flask import Flask, request, jsonify, abort, Blueprint
from model.amenity import Amenity
from persistence.DataManager import DataManager

amenity_blueprint = Blueprint('amenity_manager', __name__)
data_manager = DataManager()


@amenity_blueprint.route('/amenity', methods=['POST'])
def create_amenity():
    if not request.json or not 'name' in request.json:
        abort(400, description="Missing required fields")

    name = request.json['name']

    existing_amenities = [amenity for amenity in data_manager.storage.get(
        'Amenity', {}).values() if amenity.name == name]
    if existing_amenities:
        abort(409, description="Amenity name already exists")

    amenity = Amenity(name=name)
    data_manager.save(amenity)

    return jsonify(amenity.to_dict()), 201


@amenity_blueprint.route('/amenity', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict()
                 for amenity in data_manager.storage.get('Amenity', {}).values()]
    return jsonify(amenities), 200


@amenity_blueprint.route('/amenity/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity.to_dict()), 200


@amenity_blueprint.route('/amenity/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        abort(404, description="Amenity not found")

    if not request.json:
        abort(400, description="Missing required fields")

    name = request.json.get('name', amenity.name)

    existing_amenities = [a for a in data_manager.storage.get(
        'Amenity', {}).values() if a.name == name and a.id != amenity_id]
    if existing_amenities:
        abort(409, description="Amenity name already exists")

    amenity.name = name
    data_manager.update(amenity)
    return jsonify(amenity.to_dict()), 200


@amenity_blueprint.route('/amenity/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        abort(404, description="Amenity not found")
    data_manager.delete(amenity_id, 'Amenity')
    return '', 204