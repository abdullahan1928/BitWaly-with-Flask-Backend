from flask import request, jsonify
import jwt
from ..models.user import User 

jwt_secret = 'thisismysecretforjsonwebtoken'


async def fetch_admin(func):
    async def wrapper(*args, **kwargs):
        auth_header = request.headers.get('authToken')

        # Cannot proceed if the user is not authenticated
        if not auth_header:
            return jsonify({"error": "Not authenticated"}), 401

        try:
            data = jwt.decode(auth_header, jwt_secret)
            user_id = data.get('user_id')

            # Check if the token is valid
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401

            # Fetch the user from the database
            user = User.find_by_id(user_id)

            # Check if the user exists
            if not user:
                return jsonify({"error": "User not found"}), 401

            # Check if the user is an admin
            if user.role == 'admin':
                return await func(*args, **kwargs)
            else:
                return jsonify({"error": "Unauthorized access"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            print(e)
            return jsonify({"error": "Some error occurred"}), 500

    return wrapper
