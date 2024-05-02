#!/usr/bin/python3
"""
This file contains the Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/places/get.yml', methods=['GET'])
def get_all_places(city_id):
    """ list cities by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places/get_id.yml', methods=['GET'])
def get_place(place_id):
    """ get place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/places/delete.yml', methods=['DELETE'])
def del_place(place_id):
    """ delete place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/post.yml', methods=['POST'])
def create_obj_place(city_id):
    """ create new instance """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs = request.get_json()
    kwargs['city_id'] = city_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    obj = Place(**kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def post_place(place_id):
    """ update by id """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_places_by_id():
    """ search places by id """
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

# #!/usr/bin/python3
# """
# route for handling Place objects and operations
# """
# from flask import jsonify, abort, request
# from api.v1.views import app_views, storage
# from models.place import Place


# @app_views.route("/cities/<city_id>/places", methods=["GET"],
#                  strict_slashes=False)
# def places_by_city(city_id):
#     """
#     retrieves all Place objects by city
#     :return: json of all Places
#     """
#     place_list = []
#     city_obj = storage.get("City", str(city_id))
#     for obj in city_obj.places:
#         place_list.append(obj.to_json())

#     return jsonify(place_list)


# @app_views.route("/cities/<city_id>/places", methods=["POST"],
#                  strict_slashes=False)
# def place_create(city_id):
#     """
#     create place route
#     :return: newly created Place obj
#     """
#     place_json = request.get_json(silent=True)
#     if place_json is None:
#         abort(400, 'Not a JSON')
#     if not storage.get("User", place_json["user_id"]):
#         abort(404)
#     if not storage.get("City", city_id):
#         abort(404)
#     if "user_id" not in place_json:
#         abort(400, 'Missing user_id')
#     if "name" not in place_json:
#         abort(400, 'Missing name')

#     place_json["city_id"] = city_id

#     new_place = Place(**place_json)
#     new_place.save()
#     resp = jsonify(new_place.to_json())
#     resp.status_code = 201

#     return resp


# @app_views.route("/places/<place_id>",  methods=["GET"],
#                  strict_slashes=False)
# def place_by_id(place_id):
#     """
#     gets a specific Place object by ID
#     :param place_id: place object id
#     :return: place obj with the specified id or error
#     """

#     fetched_obj = storage.get("Place", str(place_id))

#     if fetched_obj is None:
#         abort(404)

#     return jsonify(fetched_obj.to_json())


# @app_views.route("/places/<place_id>",  methods=["PUT"],
#                  strict_slashes=False)
# def place_put(place_id):
#     """
#     updates specific Place object by ID
#     :param place_id: Place object ID
#     :return: Place object and 200 on success, or 400 or 404 on failure
#     """
#     place_json = request.get_json(silent=True)

#     if place_json is None:
#         abort(400, 'Not a JSON')

#     fetched_obj = storage.get("Place", str(place_id))

#     if fetched_obj is None:
#         abort(404)

#     for key, val in place_json.items():
#         if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
#             setattr(fetched_obj, key, val)

#     fetched_obj.save()

#     return jsonify(fetched_obj.to_json())


# @app_views.route("/places/<place_id>",  methods=["DELETE"],
#                  strict_slashes=False)
# def place_delete_by_id(place_id):
#     """
#     deletes Place by id
#     :param place_id: Place object id
#     :return: empty dict with 200 or 404 if not found
#     """

#     fetched_obj = storage.get("Place", str(place_id))

#     if fetched_obj is None:
#         abort(404)

#     storage.delete(fetched_obj)
#     storage.save()

#     return jsonify({})

# #!/usr/bin/python3
# """
# This file contains the Place module
# """
# from api.v1.views import app_views
# from flask import jsonify, abort, request, make_response
# from models import storage
# from models.place import Place
# from models.city import City
# from models.user import User
# from models.amenity import Amenity
# from models.state import State
# from flasgger.utils import swag_from


# @app_views.route('/cities/<string:city_id>/places',
#                  methods=['GET'], strict_slashes=False)
# @swag_from('documentation/places/get.yml', methods=['GET'])
# def get_all_places(city_id):
#     """ list cities by id """
#     city = storage.get(City, city_id)
#     if city is None:
#         abort(404)
#     places = [obj.to_dict() for obj in city.places]
#     return jsonify(places)


# @app_views.route('/places/<string:place_id>', methods=['GET'],
#                  strict_slashes=False)
# @swag_from('documentation/places/get_id.yml', methods=['GET'])
# def get_place(place_id):
#     """ get place by id """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     return jsonify(place.to_dict())


# @app_views.route('/places/<string:place_id>', methods=['DELETE'],
#                  strict_slashes=False)
# @swag_from('documentation/places/delete.yml', methods=['DELETE'])
# def del_place(place_id):
#     """ delete place by id """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     place.delete()
#     storage.save()
#     return jsonify({})


# @app_views.route('/cities/<string:city_id>/places', methods=['POST'],
#                  strict_slashes=False)
# @swag_from('documentation/places/post.yml', methods=['POST'])
# def create_obj_place(city_id):
#     """ create new instance """
#     city = storage.get(City, city_id)
#     if city is None:
#         abort(404)
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     if 'user_id' not in request.get_json():
#         return make_response(jsonify({"error": "Missing user_id"}), 400)
#     if 'name' not in request.get_json():
#         return make_response(jsonify({"error": "Missing name"}), 400)
#     kwargs = request.get_json()
#     kwargs['city_id'] = city_id
#     user = storage.get(User, kwargs['user_id'])
#     if user is None:
#         abort(404)
#     obj = Place(**kwargs)
#     obj.save()
#     return (jsonify(obj.to_dict()), 201)


# @app_views.route('/places/<string:place_id>', methods=['PUT'],
#                  strict_slashes=False)
# @swag_from('documentation/places/put.yml', methods=['PUT'])
# def post_place(place_id):
#     """ update by id """
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     obj = storage.get(Place, place_id)
#     if obj is None:
#         abort(404)
#     for key, value in request.get_json().items():
#         if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
#             setattr(obj, key, value)
#     storage.save()
#     return jsonify(obj.to_dict())


# @app_views.route('/places_search', methods=['POST'],
#                  strict_slashes=False)
# @swag_from('documentation/places/search.yml', methods=['POST'])
# def search_places_by_id():
#     """ search places by id """
#     if request.get_json() is None:
#         return make_response(jsonify({"error": "Not a JSON"}), 400)

#     data = request.get_json()

#     if data and len(data):
#         states = data.get('states', None)
#         cities = data.get('cities', None)
#         amenities = data.get('amenities', None)

#     if not data or not len(data) or (
#             not states and
#             not cities and
#             not amenities):
#         places = storage.all(Place).values()
#         list_places = []
#         for place in places:
#             list_places.append(place.to_dict())
#         return jsonify(list_places)

#     list_places = []
#     if states:
#         states_obj = [storage.get(State, s_id) for s_id in states]
#         for state in states_obj:
#             if state:
#                 for city in state.cities:
#                     if city:
#                         for place in city.places:
#                             list_places.append(place)

#     if cities:
#         city_obj = [storage.get(City, c_id) for c_id in cities]
#         for city in city_obj:
#             if city:
#                 for place in city.places:
#                     if place not in list_places:
#                         list_places.append(place)

#     if amenities:
#         if not list_places:
#             list_places = storage.all(Place).values()
#         amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
#         list_places = [place for place in list_places
#                        if all([am in place.amenities
#                                for am in amenities_obj])]

#     places = []
#     for p in list_places:
#         d = p.to_dict()
#         d.pop('amenities', None)
#         places.append(d)

#     return jsonify(places)
