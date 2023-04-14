#!/usr/bin/python3
""" View for amenity"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def show_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""
    post = request.get_json()
    if post is None:
        abort(400, 'Not a JSON')
    if 'name' not in post:
        abort(400, 'Missing name')
    amenity = Amenity(**post)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    put = request.get_json()
    if put is None:
        abort(400, 'Not a JSON')
    for k, v in put.items():
        ignore_keys = ['id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
