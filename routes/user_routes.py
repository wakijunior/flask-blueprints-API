from flask import Blueprint, jsonify
from models import User
from database import get_db
from decorators import role_required

users = Blueprint("users", __name__)

@users.route("/users", methods=["GET"])
# @role_required("admin")
def get_users():

    with get_db() as db:

        users = db.query(User).all()

        return jsonify([
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ])