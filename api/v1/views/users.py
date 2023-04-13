#!/usr/bin/python3
""" View for user"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def show_users():
    """Retrieves the list of all User objects"""
    all_users = []
    users = storage.all(User).values()
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    post = request.get_json()
    if post is None:
        abort(400, 'Not a JSON')
    if 'email' not in post:
        abort(400, 'Missing email')
    if 'password' not in post:
        abort(400, 'Missing password')
    user = User(**post)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    put = request.get_json()
    if put is None:
        abort(400, 'Not a JSON')
    for k, v in put.items():
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
