#!/usr/bin/python3
"""This module contain API for model class User"""
from models import storage
import uuid
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieve all users in memory"""
    users = storage.all(User)
    if not users:
        abort(404)
    users_list = [user.to_dict() for user in users.values()]
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False)
def get_user(user_id):
    """Get a User given it's ID"""
    user = storage.get(User, user_id)
    try:
        return jsonify(user.to_dict())
    except AttributeError:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_User(user_id):
    """Delete user from the the database"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Add a User to a user where it belongs"""
    try:
        data = request.get_json()
        user = User()
        user.id = data.get('id', str(uuid.uuid4()))
        user.email = data['email']
        if not data.get('password'):
            abort(400, 'Missing password')
        user.password = data.get('password')
        user.first_name = data.get('first_name', "")
        user.last_name = data.get('last_name', "")
        user.save()
        return make_response(jsonify(user.to_dict()), 201)

    except KeyError:
        abort(400, "Missing email")
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update user with new input"""
    user = storage.get(User, user_id)
    try:
        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)

    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")
