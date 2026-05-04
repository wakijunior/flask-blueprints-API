from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database import get_db
from models import User, Product, Sale, Payment
from sqlalchemy import func
from datetime import datetime, timedelta


analytics = Blueprint("analytics", __name__)

@analytics.route("/analytics/overview", methods=["GET"])
@jwt_required()
def overview():

    with get_db() as db:

        users = db.query(User).count()
        products = db.query(Product).count()
        sales = db.query(Sale).count()
        payments = db.query(Payment).count()

        revenue = db.query(
            func.sum(Payment.amount)
        ).filter(Payment.status == "Success").scalar() or 0

        return jsonify({
            "users": users,
            "products": products,
            "sales": sales,
            "payments": payments,
            "revenue": revenue
        })
        
@analytics.route("/analytics/daily-sales", methods=["GET"])
@jwt_required()
def daily_sales():
        
    range_type = request.args.get("range", "7")  # default 7 days

    with get_db() as db:

        if range_type == "30":
            start_date = datetime.now() - timedelta(days=30)
        else:
            start_date = datetime.now() - timedelta(days=7)

        results = db.query(
            func.date(Sale.created_at),
            func.count(Sale.id)
        ).filter(
            Sale.created_at >= start_date
        ).group_by(
            func.date(Sale.created_at)
        ).all()

        return jsonify([
            {
                "date": str(date),
                "sales": count
            }
            for date, count in results
        ])
        
@analytics.route("/analytics/revenue-7days", methods=["GET"])
@jwt_required()
def revenue_7days():
    with get_db() as db:

        start_date = datetime.now() - timedelta(days=7)

        results = db.query(
            func.date(Payment.created_at),
            func.sum(Payment.amount)
        ).filter(
            Payment.status == "Success",
            Payment.created_at >= start_date
        ).group_by(
            func.date(Payment.created_at)
        ).all()

        return jsonify([
            {
                "date": str(date),
                "revenue": float(amount or 0)
            }
            for date, amount in results
        ])
    
@analytics.route("/analytics/revenue", methods=["GET"])
@jwt_required()
def revenue():

    range_type = request.args.get("range", "7")

    with get_db() as db:

        if range_type == "30":
            start_date = datetime.now() - timedelta(days=30)
        else:
            start_date = datetime.now() - timedelta(days=7)

        results = db.query(
            func.date(Payment.created_at),
            func.sum(Payment.amount)
        ).filter(
            Payment.status == "Success",
            Payment.created_at >= start_date
        ).group_by(
            func.date(Payment.created_at)
        ).all()

        return jsonify([
            {
                "date": str(date),
                "revenue": float(amount or 0)
            }
            for date, amount in results
        ])
        
@analytics.route("/analytics/top-products", methods=["GET"])
@jwt_required()
def top_products():

    with get_db() as db:

        results = db.query(
            Product.product_name,
            func.count(Sale.id)
        ).join(Sale, Sale.product_id == Product.id)\
         .group_by(Product.product_name)\
         .order_by(func.count(Sale.id).desc())\
         .limit(5)\
         .all()

        return jsonify([
            {
                "product": name,
                "sales": count
            }
            for name, count in results
        ])
        
@analytics.route("/analytics/payments-status", methods=["GET"])
@jwt_required()
def payment_status():

    with get_db() as db:

        success = db.query(Payment).filter_by(status="Success").count()
        failed = db.query(Payment).filter_by(status="Failed").count()
        pending = db.query(Payment).filter_by(status="Pending").count()

        return jsonify({
            "success": success,
            "failed": failed,
            "pending": pending
        })