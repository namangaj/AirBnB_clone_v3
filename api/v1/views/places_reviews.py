#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    retrieves all Review objects by place
    :return: json of all reviews
    """
    review_list = []
    place_obj = storage.get("Place", str(place_id))

    if place_obj is None:
        abort(404)

    for obj in place_obj.reviews:
        review_list.append(obj.to_json())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """
    create REview route
    :return: newly created Review obj
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    gets a specific Review object by ID
    :param review_id: place object id
    :return: review obj with the specified id or error
    """

    fetched_obj = storage.get("Review", str(review_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    updates specific Review object by ID
    :param review_id: Review object ID
    :return: Review object and 200 on success, or 400 or 404 on failure
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("Review", str(review_id))

    if fetched_obj is None:
        abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    deletes Review by id
    :param : Review object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("Review", str(review_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})

# #!/usr/bin/python3
# """
# This file contains the Review module
# """
# from api.v1.views import app_views
# from flask import jsonify, abort, request, make_response
# from models import storage
# from models.place import Place
# from models.review import Review
# from models.user import User
# from flasgger.utils import swag_from


# @app_views.route('/places/<string:place_id>/reviews',
#                  methods=['GET'], strict_slashes=False)
# @swag_from('documentation/reviews/get.yml', methods=['GET'])
# def get_all_reviews(place_id):
#     """ get reviews from a spcific place """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     reviews = [obj.to_dict() for obj in place.reviews]
#     return jsonify(reviews)


# @app_views.route('/reviews/<string:review_id>', methods=['GET'],
#                  strict_slashes=False)
# @swag_from('documentation/reviews/get_id.yml', methods=['GET'])
# def get_review(review_id):
#     """ get review by id"""
#     review = storage.get(Review, review_id)
#     if review is None:
#         abort(404)
#     return jsonify(review.to_dict())


# @app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
#                  strict_slashes=False)
# @swag_from('documentation/reviews/delete.yml', methods=['DELETE'])
# def del_review(review_id):
#     """ delete review by id"""
#     review = storage.get(Review, review_id)
#     if review is None:
#         abort(404)
#     review.delete()
#     storage.save()
#     return jsonify({})


# @app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
#                  strict_slashes=False)
# @swag_from('documentation/reviews/post.yml', methods=['POST'])
# def create_obj_review(place_id):
#     """ create new instance """
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     if 'user_id' not in request.get_json():
#         return make_response(jsonify({"error": "Missing user_id"}), 400)
#     if 'text' not in request.get_json():
#         return make_response(jsonify({"error": "Missing text"}), 400)
#     kwargs = request.get_json()
#     kwargs['place_id'] = place_id
#     user = storage.get(User, kwargs['user_id'])
#     if user is None:
#         abort(404)
#     obj = Review(**kwargs)
#     obj.save()
#     return (jsonify(obj.to_dict()), 201)


# @app_views.route('/reviews/<string:review_id>', methods=['PUT'],
#                  strict_slashes=False)
# @swag_from('documentation/reviews/put.yml', methods=['PUT'])
# def post_review(review_id):
#     """ updates by id """
#     if not request.get_json():
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     obj = storage.get(Review, review_id)
#     if obj is None:
#         abort(404)
#     for key, value in request.get_json().items():
#         if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
#             setattr(obj, key, value)
#     storage.save()
#     return jsonify(obj.to_dict())
