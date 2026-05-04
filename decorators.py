from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify

def role_required(role):

    def wrapper(fn):

        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):

            claims = get_jwt()

            if claims.get("role") != role:
                return jsonify({
                    "error": "Access denied"
                }), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper