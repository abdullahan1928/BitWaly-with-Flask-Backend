from flask import Blueprint, request, jsonify
from app.models.formerUrl import FormerUrl
from app.middlewares.fetch_user import fetch_user
import json

# Creating a Blueprint for URL management
formerUrl_blueprint = Blueprint('formerUrl', __name__, url_prefix='/formerUrl')

# Defining routes for URL management


@formerUrl_blueprint.route("/id/<id>", methods=['GET'])
@fetch_user
def retrieve_url_by_id(id):
    user_id = request.user_id
    retrieved_url = FormerUrl.find_by_id(user_id, id)

    if retrieved_url:
        return json.dumps(retrieved_url, default=str), 200
    else:
        return jsonify({"error": "URL not found"}), 404
