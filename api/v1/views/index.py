#!/usr/bin/python3
""" Route to /status that returns 'status': 'OK'"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def show_status():
    return {
        'status': 'OK'
    }


@app_views.route('/stats', strict_slashes=False)
def show_stats():
    classes = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(classes)
