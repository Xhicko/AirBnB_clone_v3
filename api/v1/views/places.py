#!/usr/bin/python3
"""This module contain API for model class Place"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<string:city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieve all places in a certain city"""
    city = storage.get(City, city_id)
    try:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    except AttributeError:
        abort(404)


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False)
def get_place(place_id):
    """Get a Place given it's ID"""
    place = storage.get(Place, place_id)
    try:
        return jsonify(place.to_dict())
    except AttributeError:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete place from the the database"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """Creates a new place object and assign it on new city"""
    city = storage.get(City, city_id)
    try:
        data = request.get_json()
        place = Place()
        place.id = data.get('id', place.id)
        place.user_id = storage.get(User, data['user_id']).id
        place.city_id = city.id
        if not data.get('name'):
            abort(400, 'Missing name')
        place.name = data.get('name')
        place.description = data.get('description', "")
        place.number_rooms = data.get('number_rooms', 0)
        place.number_bathrooms = data.get('number_bathrooms', 0)
        place.max_guest = data.get('max_guests', 0)
        place.price_by_night = data.get('price_by_night', 0)
        place.latitude = data.get('latitude')
        place.longitude = data.get('longitude')
        place.save()
        return make_response(jsonify(place.to_dict()), 201)

    except KeyError:
        abort(400, "Missing user_id")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update place with new input"""
    place = storage.get(Place, place_id)
    try:
        data = request.get_json()
        place.name = data.get('name', place.name)
        place.description = data.get('description', place.description)
        place.number_rooms = data.get('number_rooms', place.number_rooms)
        place.number_bathrooms = data.get('number_bathrooms',
                                          place.number_bathrooms)
        place.max_guest = data.get('max_guests', place.max_guests)
        place.price_by_night = data.get('price_by_night',
                                        place.price_by_night)
        place.latitude = data.get('latitude', place.latitude)
        place.longitude = data.get('longitude', place.longitude)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)

    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")
