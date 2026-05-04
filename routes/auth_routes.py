from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models import User
from database import get_db
from extensions import bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():

    with get_db() as db:

        data = request.get_json()

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "customer")

        existing_user = db.query(User).filter_by(email=email).first()

        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            role=role
        )

        db.add(user)
        db.commit()

        token = create_access_token(identity={
                                "id": user.id,
                                "email": user.email,
                                "role": user.role
                            })
        
        return jsonify({
            "message": "Registration successful",
            "token": token,
            "role": user.role
        }), 201


@auth.route("/login", methods=["POST"])
def login():

    with get_db() as db:

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = db.query(User).filter_by(email=email).first()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if bcrypt.check_password_hash(user.password, password):

            token = create_access_token(
                identity=user.email,
                additional_claims={
                    "id": user.id,
                    "role": user.role
                }
            )

            return jsonify({
                "message": "Login successful",
                "access_token": token,
                "role": user.role
            })

        return jsonify({"error": "Invalid credentials"}), 401


@auth.route("/me", methods=["GET"])
@jwt_required()
def me():

    claims = get_jwt()

    return jsonify({
        "email": claims["sub"],
        "role": claims.get("role")
    })