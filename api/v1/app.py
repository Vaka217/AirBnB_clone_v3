#!/usr/bin/python3
""" Create Flask app, register blueprint and runs app"""
from os import getenv
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Page not found error handler"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    h, p = '0.0.0.0', '5000'
    if getenv('HBNB_API_HOST'):
        h = getenv('HBNB_API_HOST')
    if getenv('HBNB_API_PORT'):
        p = getenv('HBNB_API_PORT')
    app.run(host=h, port=p, threaded=True)
