from flask import Flask, request, jsonify, abort, Blueprint
from model.place import Place
from persistence.DataManager import DataManager


place_manager_blueprint = Blueprint('place_manager', __name__)
data_manager = DataManager()


@place_manager_blueprint.route('/places', methods=['POST'])
def create_place():
    required_fields = ['name', 'address', 'city_id', 'latitude', 'longitude', 'host_id',
                       'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests']
    if not request.json or not all(field in request.json for field in required_fields):
        abort(400, description="Missing required fields")

    data = request.json
    name = data['name']
    description = data.get('description', '')
    address = data['address']
    city_id = data['city_id']
    latitude = data['latitude']
    longitude = data['longitude']
    host_id = data['host_id']
    number_of_rooms = data['number_of_rooms']
    number_of_bathrooms = data['number_of_bathrooms']
    price_per_night = data['price_per_night']
    max_guests = data['max_guests']
    amenity_ids = data.get('amenity_ids', [])

    # Validar existencia de city_id
    if not data_manager.get(city_id, 'City'):
        abort(400, description="Invalid city_id")

    # Validar existencia de amenity_ids
    for amenity_id in amenity_ids:
        if not data_manager.get(amenity_id, 'Amenity'):
            abort(400, description=f"Invalid amenity_id: {amenity_id}")

    place = Place(name=name, description=description, address=address, city_id=city_id, latitude=latitude, longitude=longitude,
                  host_id=host_id, number_of_rooms=number_of_rooms, number_of_bathrooms=number_of_bathrooms,
                  price_per_night=price_per_night, max_guests=max_guests, amenity_ids=amenity_ids)
    data_manager.save(place)

    return jsonify(place.to_dict()), 201


@place_manager_blueprint.route('/places', methods=['GET'])
def get_places():
    places = [place.to_dict()
              for place in data_manager.storage.get('Place', {}).values()]
    return jsonify(places), 200


@place_manager_blueprint.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")
    return jsonify(place.to_dict()), 200


@place_manager_blueprint.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")

    if not request.json:
        abort(400, description="Missing required fields")

    data = request.json
    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    place.address = data.get('address', place.address)
    if 'city_id' in data:
        place.city_id = data['city_id']
        if not data_manager.get(place.city_id, 'City'):
            abort(400, description="Invalid city_id")
    place.latitude = data.get('latitude', place.latitude)
    place.longitude = data.get('longitude', place.longitude)
    place.host_id = data.get('host_id', place.host_id)
    place.number_of_rooms = data.get('number_of_rooms', place.number_of_rooms)
    place.number_of_bathrooms = data.get(
        'number_of_bathrooms', place.number_of_bathrooms)
    place.price_per_night = data.get('price_per_night', place.price_per_night)
    place.max_guests = data.get('max_guests', place.max_guests)
    place.amenity_ids = data.get('amenity_ids', place.amenity_ids)

    # Validar existencia de amenity_ids
    for amenity_id in place.amenity_ids:
        if not data_manager.get(amenity_id, 'Amenity'):
            abort(400, description=f"Invalid amenity_id: {amenity_id}")

    data_manager.update(place)
    return jsonify(place.to_dict()), 200


@place_manager_blueprint.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")
    data_manager.delete(place_id, 'Place')
    return '', 204