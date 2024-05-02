#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    get all amenities of a place
    :param place_id: amenity id
    :return: all amenities
    """
    fetched_obj = storage.get("Place", str(place_id))

    all_amenities = []

    if fetched_obj is None:
        abort(404)

    for obj in fetched_obj.amenities:
        all_amenities.append(obj.to_json())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    unlinks an amenity in a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: empty dict or error
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetched_obj = storage.get("Place", place_id)
    found = 0

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetched_obj.amenities.remove(obj)
            else:
                fetched_obj.amenity_ids.remove(obj.id)
            fetched_obj.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        resp = jsonify({})
        resp.status_code = 201
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    links a amenity with a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: return Amenity obj added or error
    """

    fetched_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    found_amenity = None

    if not fetched_obj or not amenity_obj:
        abort(404)

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            found_amenity = obj
            break

    if found_amenity is not None:
        return jsonify(found_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_obj.amenities.append(amenity_obj)
    else:
        fetched_obj.amenities = amenity_obj

    fetched_obj.save()

    resp = jsonify(amenity_obj.to_json())
    resp.status_code = 201

    return resp


# #!/usr/bin/python3
# """places_amenities.py"""
# import os
# from api.v1.views import app_views
# from flask import abort, jsonify, make_response, request
# from models import storage
# from models.amenity import Amenity
# from models.place import Place
# from flasgger.utils import swag_from


# @app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
#                  strict_slashes=False)
# @swag_from('documentation/place_amenity/get_id.yml', methods=['GET'])
# def get_amenities(place_id):
#     """ retrieves all amenities from a place """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     amenities = [obj.to_dict() for obj in place.amenities]
#     return jsonify(amenities)


# @app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
#                  methods=['DELETE'], strict_slashes=False)
# @swag_from('documentation/place_amenity/delete.yml', methods=['DELETE'])
# def delete_amenity(place_id, amenity_id):
#     """ delete amenity from place """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     amenity = storage.get(Amenity, amenity_id)
#     if amenity is None:
#         abort(404)
#     if amenity not in place.amenities:
#         abort(404)
#     place.amenities.remove(amenity)
#     storage.save()
#     return jsonify({})


# @app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
#                  methods=['POST'], strict_slashes=False)
# @swag_from('documentation/place_amenity/post.yml', methods=['POST'])
# def post_amenity2(place_id, amenity_id):
#     """ post amenity by id """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     amenity = storage.get(Amenity, amenity_id)
#     if amenity is None:
#         abort(404)
#     if amenity in place.amenities:
#         return (jsonify(amenity.to_dict()), 200)
#     place.amenities.append(obj)
#     storage.save()
#     return (jsonify(amenity.to_dict(), 201))
