from flask import Blueprint, request, jsonify
from ..models.user import User
from ..middlewares.fetch_user import fetch_user
import bcrypt
import jwt
import json

jwt_secret = 'thisismysecretforjsonwebtoken'

# Creating a Blueprint for user authentication and account management
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# Controller for user signup


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user already exists
    if User.find_by_email(email):
        return jsonify({"error": "User already exists"}), 422

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode(
        'utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create new user
    new_user = User(email=email, password=hashed_password)
    new_user.save()

    # Generate JWT token
    auth_token = jwt.encode({'user_id': str(new_user.id)}, jwt_secret)

    return jsonify({"auth_token": auth_token.decode('utf-8')}), 201

# Controller for user signin


@auth_blueprint.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Find user by email
    user = User.find_by_email(email)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 422

    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 422

    # Generate JWT token
    auth_token = jwt.encode({'user_id': str(user["_id"])}, jwt_secret)

    role = user.get('role', 'user')

    return jsonify({"authToken": auth_token, "role": role}), 200

# Controller to get user details


@auth_blueprint.route('/getUser', methods=['GET'])
@fetch_user
def get_user():
    user_id = request.user_id
    user = User.find_by_id(user_id)
    
    if user:
        return json.dumps(user, default=str), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Controller to update user's name


@auth_blueprint.route('/user/name', methods=['PUT'])
@fetch_user
def update_name():
    user_id = request.user_id
    data = request.get_json()
    new_name = data.get('name')
    user = User.find_by_id(user_id)
    if user:
        user.name = new_name
        user.save()
        return jsonify({"user": user.to_json()}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Controller to update user's password


@auth_blueprint.route('/user/password', methods=['PUT'])
@fetch_user
def update_password():
    user_id = request.user_id
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    user = User.find_by_id(user_id)
    if user and bcrypt.checkpw(old_password.encode('utf-8'), user['password'].encode('utf-8')):
        hashed_password = bcrypt.hashpw(new_password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        user['password'] = hashed_password
        user.save()
        return jsonify({"user": user.to_json()}), 200
    else:
        return jsonify({"error": "Invalid password"}), 422

# Controller to delete user account


@auth_blueprint.route('/user', methods=['DELETE'])
@fetch_user
def delete_account():
    user_id = request.user_id
    user = User.find_by_id(user_id)
    if user:
        user.delete()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
