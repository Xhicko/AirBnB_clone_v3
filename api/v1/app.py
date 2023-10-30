#!/usr/bin/python3
"""This module contain a flask application that deals with APIs"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(exception):
    """Call storage.close to close a session and get another"""
    storage.close()


@app.errorhandler(404)
def handle404(error):
    """Handle error, 404"""
    resp = jsonify({"error": "Not found"})
    resp.status_code = 404
    return resp


@app.errorhandler(400)
def handle400(error):
    """Handle 400 error"""
    return make_response(jsonify({"error": error.description}), 400)


if __name__ == '__main__':
    import os
    host = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
