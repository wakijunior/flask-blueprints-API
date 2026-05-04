from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from models import Order
from database import get_db

sales = Blueprint("sales", __name__)


@sales.route("/sales", methods=["GET"])
@jwt_required()
def get_sales():

    with get_db() as db:
        results = db.query(
            func.date(Order.created_at),
            func.sum(Order.total_amount)
        ).filter(
            Order.status == "PAID"
        ).group_by(
            func.date(Order.created_at)
        ).all()

        data = [
            {"date": str(r[0]), "total_sales": float(r[1])}
            for r in results
        ]

        return jsonify(data)