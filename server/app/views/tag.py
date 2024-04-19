from flask import Blueprint, request, jsonify
from app.models.tag import Tag
from app.middlewares.fetch_user import fetch_user
import json

tag_blueprint = Blueprint("tag_blueprint", __name__, url_prefix='/tag')


@tag_blueprint.route("", methods=["POST"])
@fetch_user
def create_tag():
    user_id = request.user_id
    data = request.json
    url = data.get("url")
    tag_name = data.get("tag")

    if not url or not tag_name:
        return jsonify({"error": "URL and tag name are required"}), 400

    new_tag = Tag.create_tag(user_id, url, tag_name)

    return json.dumps(new_tag, default=str), 200


@tag_blueprint.route("", methods=["GET"])
@fetch_user
def get_all_tags():
    user_id = request.user_id
    tags = Tag.find_by_user(user_id)

    if tags:
        return json.dumps(tags, default=str), 200
    else:
        return jsonify({"error": "No tags found for the user"}), 404


@tag_blueprint.route("/<url_id>", methods=["GET"])
@fetch_user
def get_tag_by_url_id(url_id):
    user_id = request.user_id
    tags = Tag.find_by_url(user_id, url_id)

    if tags:
        return json.dumps(tags, default=str), 200
    else:
        return jsonify({"error": "Tag not found"}), 404


@tag_blueprint.route("/<id>", methods=["DELETE"])
@fetch_user
def delete_tag(id):
    user_id = request.user_id
    deleted_count = Tag.delete_by_id(user_id, id)
    if deleted_count:
        return jsonify({"message": "Tag deleted successfully"}), 200
    else:
        return jsonify({"error": "Tag not found"}), 404
