#!/usr/bin/python3
"""This module contain API for model class Review"""
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<string:place_id>/reviews',
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Get all reviews for a certain place"""
    place = storage.get(Place, place_id)
    try:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    except AttributeError:
        abort(404)


@app_views.route('/reviews/<string:review_id>',
                 strict_slashes=False)
def get_review(review_id):
    """Get a review given it's ID"""
    review = storage.get(Review, review_id)
    try:
        return jsonify(review.to_dict())
    except AttributeError:
        abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review from the the database"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """Add a review to a place"""
    place = storage.get(Place, place_id)
    try:
        data = request.get_json()
        review = Review()
        review.id = data.get('id', review.id)
        review.user_id = storage.get(User, data['user_id']).id
        review.place_id = place.id
        if not data.get('text'):
            abort(400, "Missing text")
        review.text = data.get('text')
        review.save()
        return make_response(jsonify(review.to_dict()), 201)
    except KeyError:
        abort(400, "Missing user_id")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update review with new input"""
    review = storage.get(Review, review_id)
    try:
        data = request.get_json()
        if data['text'] and type(data['text']) is str:
            review.name = data.get('name')
            review.save()
            return make_response(jsonify(review.to_dict()), 200)
    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")
