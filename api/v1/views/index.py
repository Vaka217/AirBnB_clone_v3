#!/usr/bin/python3
""" Route to /status that returns 'status': 'OK'"""
from api.v1.views import app_views

@app_views.route('/status')
def show_status(page):
    return {
        'status': 'OK'
    }
