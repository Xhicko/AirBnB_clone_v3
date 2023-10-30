#!/usr/bin/python3
"""This module contain API for model class State"""
from models import storage
import uuid
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve all states in memory"""
    states = storage.all(State)
    if not states:
        abort(404)
    states_dict = [state.to_dict() for state in states.values()]
    return jsonify(states_dict)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Get a State given it's ID"""
    state = storage.get(State, state_id)
    try:
        return jsonify(state.to_dict())
    except AttributeError:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state from the the database"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """Add a State to a state where it belongs"""
    try:
        data = request.get_json()
        state = State()
        state.id = data.get('id', str(uuid.uuid4()))
        state.name = data['name']
        state.save()
        return make_response(jsonify(state.to_dict()), 201)

    except KeyError:
        abort(400, "Missing name")
    except Exception as e:
        abort(400, "Not a JSON")


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update state with new input"""
    state = storage.get(State, state_id)
    try:
        data = request.get_json()
        if data['name'] and type(data['name']) is str:
            state.name = data.get('name')
            state.save()
        return make_response(jsonify(state.to_dict()), 201)

    except KeyError:
        abort(400, "Missing name")
    except AttributeError:
        abort(404)
    except Exception:
        abort(400, "Not a JSON")
