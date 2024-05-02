#!/usr/bin/python3

#!/usr/bin/python3
"""
Createw Flask app; app_view
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route
    :return: response with json
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp

# """
# This module contains endpoint(route) status
# """
# from models import storage
# from flask import Flask
# from api.v1.views import app_views
# from flask import jsonify


# @app_views.route('/status', strict_slashes=False)
# def status():
#     """
#     Returns a JSON status
#     """
#     return jsonify({"status": "OK"})


# @app_views.route('/stats', strict_slashes=False)
# def count():
#     """
#     Retrieves the number of each objects by type
#     """
#     return jsonify({"amenities": storage.count("Amenity"),
#                     "cities": storage.count("City"),
#                     "places": storage.count("Place"),
#                     "reviews": storage.count("Review"),
#                     "states": storage.count("State"),
#                     "users": storage.count("User")})
