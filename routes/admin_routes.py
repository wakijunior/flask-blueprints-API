from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models import User, Product, Sale

admin = Blueprint("admin", __name__)

@admin.route("/admin/dashboard", methods=["GET"])
@jwt_required
def admin_dashboard():
    with get_db() as db:

        users_count = db.query(User).count()
        products_count = db.query(Product).count()
        sales_count = db.query(Sale).count()

        return jsonify({
            "users": users_count,
            "products": products_count,
            "sales": sales_count
        }), 200