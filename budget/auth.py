from flask import Blueprint, jsonify, request
from .database import db_session
from .models import User
from datetime import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS


auth = Blueprint('auth', __name__)

CORS(auth)

jwt = JWTManager()
bcrypt = Bcrypt()


allowed_methods = ['POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
# ------------------ REGISTER ------------------
@auth.route('/register', methods=allowed_methods)
def register():
    try:
        if not request.method == "POST":
            return jsonify({"message": "Send a POST request to register a user"}), 405
        
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request must be JSON"}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400

        username = username.strip().lower()

        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            username=username,
            password=hashed_password,
            created_at=datetime.utcnow()
        )

        db_session.add(new_user)
        db_session.commit()

        # ✅ Use user.id
        token = create_access_token(identity=new_user.username)

        return jsonify({
            "message": "User registered successfully!",
            "token": token
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500


# ------------------ LOGIN ------------------
@auth.route('/login', methods=allowed_methods)
def login():
    try:
        if not request.method == "POST":
            return jsonify({"message": "Send a POST request to login"}), 405
        
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request must be JSON"}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400

        username = username.strip().lower()

        user = db_session.query(User).filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            token = create_access_token(identity=user.username)

            return jsonify({
                "message": "Login successful!",
                "token": token
            }), 200

        return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
