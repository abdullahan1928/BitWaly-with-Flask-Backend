from flask import Blueprint, request, jsonify
from app.models.url import Url
from app.middlewares.fetch_user import fetch_user
import json

# Creating a Blueprint for URL management
url_blueprint = Blueprint('url', __name__, url_prefix='/url')

# Defining routes for URL management


@url_blueprint.route("/retreive/<short_url>", methods=['POST'])
def retrieve_url(short_url):
    retrieved_url = Url.find_by_short_url(short_url)
    if retrieved_url:
        return json.dumps(retrieved_url, default=str), 200
    else:
        return jsonify({"error": "URL not found"}), 404


@url_blueprint.route("/retreive/id/<id>", methods=['GET'])
@fetch_user
def retrieve_url_by_id(id):
    user_id = request.user_id
    retrieved_url = Url.find_by_id(user_id, id)

    if retrieved_url:
        return json.dumps(retrieved_url, default=str), 200
    else:
        return jsonify({"error": "URL not found"}), 404


@url_blueprint.route("/userUrls", methods=['GET'])
@fetch_user
def retrieve_urls_for_user():
    user_id = request.user_id
    user_urls = Url.find_by_user_id(user_id)
    return json.dumps(user_urls, default=str), 200


@url_blueprint.route("/shorten", methods=['POST'])
@fetch_user
def shorten_url():
    user_id = request.user_id
    data = request.get_json()
    original_url = data.get('original_url')
    short_url = data.get('short_url')
    shard_key = data.get('shard_key')
    title = data.get('title')
    image = data.get('image')
    is_custom = data.get('is_custom')
    tags = data.get('tags')
    former_urls = data.get('former_urls')
    if original_url and short_url and shard_key:
        new_url = Url.shorten_url(user_id, original_url, short_url,
                                  shard_key, title, image, is_custom, tags, former_urls)
        return jsonify(new_url), 201
    else:
        return jsonify({"error": "Incomplete data provided"}), 400


@url_blueprint.route("/update/<id>", methods=['PUT'])
@fetch_user
def update_url(id):
    user_id = request.user_id
    update_data = request.get_json()
    updated_url = Url.update_url(user_id, id, update_data)
    if updated_url:
        return jsonify(updated_url), 200
    else:
        return jsonify({"error": "URL not found or unauthorized"}), 404


@url_blueprint.route("/delete/<id>", methods=['DELETE'])
@fetch_user
def delete_url(id):
    user_id = request.user_id
    deleted_url = Url.delete_url(user_id, id)
    if deleted_url:
        return jsonify(deleted_url), 200
    else:
        return jsonify({"error": "URL not found or unauthorized"}), 404
