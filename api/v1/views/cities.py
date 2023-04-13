#!/usr/bin/python3
""" View for City"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def show_cities(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = []
    cities = storage.all(City).values()
    for city in cities:
        if city.state_id != state_id:
            continue
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    post = request.get_json()
    if post is None:
        abort(400, 'Not a JSON')
    if 'name' not in post:
        abort(400, 'Missing name')
    city = City(**post)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    put = request.get_json()
    if put is None:
        abort(400, 'Not a JSON')
    for k, v in put.items():
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
