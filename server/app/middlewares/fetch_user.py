from functools import wraps
from flask import request, jsonify
import jwt

jwt_secret = 'thisismysecretforjsonwebtoken'

def fetch_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('authToken')

        if not auth_header:
            return jsonify({"error": "Not authenticated"}), 401

        try:
            data = jwt.decode(auth_header, jwt_secret, algorithms=['HS256'])
            request.user_id = data['user_id']

            return func(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": "Some error occurred"}), 500

    return wrapper