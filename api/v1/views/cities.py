#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_json())

    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """

    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})

# #!/usr/bin/python3
# """
# This file contains the City module
# """
# from api.v1.views import app_views
# from flask import jsonify, abort, request, make_response
# from models import storage
# from models.state import State
# from models.city import City
# from flasgger.utils import swag_from


# @app_views.route('/states/<string:state_id>/cities',
#                  methods=['GET'], strict_slashes=False)
# @swag_from('documentation/city/get.yml', methods=['GET'])
# def get_cities(state_id):
#     """ Gets cities for state_id """
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     list_cities = [obj.to_dict() for obj in state.cities]
#     return jsonify(list_cities)


# @app_views.route('/cities/<string:city_id>', methods=['GET'],
#                  strict_slashes=False)
# @swag_from('documentation/city/get_id.yml', methods=['GET'])
# def get_city(city_id):
#     """ get city by id"""
#     city = storage.get(City, city_id)
#     if city is None:
#         abort(404)
#     return jsonify(city.to_dict())


# @app_views.route('/cities/<string:city_id>', methods=['DELETE'],
#                  strict_slashes=False)
# @swag_from('documentation/city/delete.yml', methods=['DELETE'])
# def del_city(city_id):
#     """ delete city by id"""
#     city = storage.get(City, city_id)
#     if city is None:
#         abort(404)
#     city.delete()
#     storage.save()
#     return jsonify({})


# @app_views.route('/states/<string:state_id>/cities', methods=['POST'],
#                  strict_slashes=False)
# @swag_from('documentation/city/post.yml', methods=['POST'])
# def create_obj_city(state_id):
#     """ create new instance """
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     if 'name' not in request.get_json():
#         return make_response(jsonify({"error": "Missing name"}), 400)

#     js = request.get_json()
#     obj = City(**js)
#     obj.state_id = state.id
#     obj.save()
#     return jsonify(obj.to_dict()), 201


# @app_views.route('/cities/<string:city_id>', methods=['PUT'],
#                  strict_slashes=False)
# @swag_from('documentation/city/put.yml', methods=['PUT'])
# def post_city(city_id):
#     """  """
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     obj = storage.get(City, city_id)
#     if obj is None:
#         abort(404)
#     for key, value in request.get_json().items():
#         if key not in ['id', 'state_id', 'created_at', 'updated_at']:
#             setattr(obj, key, value)
#     storage.save()
#     return jsonify(obj.to_dict())
