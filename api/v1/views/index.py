#!/usr/bin/python3
"""
createw Flask app; app_views.
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """
    status route
    :return: response with json
    """
    response = {'status': "OK"}
    return jsonify(response)
