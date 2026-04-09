from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .database import db_session
from .auth import allowed_methods
from datetime import datetime
from .models import Budget, User
from . import jwt

addbudget = Blueprint('addbudget', __name__)

# ------------------ BUDGET ------------------
@addbudget.route('/budget', methods=allowed_methods)
@jwt_required()
def budget():
    try:
        if request.method == "POST":

            # Check login
            current_username = get_jwt_identity()
        
            if not current_username:
                return jsonify({"error": "Unauthorized"}), 401

            # POST → Add budget
            
            data = request.get_json()

            if not data:
                return jsonify({"error": "Request must be JSON"}), 400

            title = data.get('title')
            amount = data.get('amount')
            date = data.get('date')

            if not title or amount is None or not date:
                return jsonify({"error": "All fields are required"}), 400

            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
            except:
                return jsonify({"error": "Invalid date format"}), 400

            user = db_session.query(User).filter_by(username=current_username).first()
            
            if not user:
                 return jsonify({"error": "User not found"}), 404

            new_budget = Budget(
                title=title,
                amount=float(amount),
                date=date_obj,
                user_id=user.id
            )

            db_session.add(new_budget)
            db_session.commit()

            return jsonify({"message": "Budget added"}), 201
        elif request.method == "GET":
            
            current_username = get_jwt_identity()

            user = db_session.query(User).filter_by(username=current_username).first()

            # GET → Fetch budgets
            budgets = db_session.query(Budget).filter_by(user_id=user.id).all()

            return jsonify([
                {
                    "id": b.id,
                    "title": b.title,
                    "amount": b.amount,
                    "date": b.date.strftime("%Y-%m-%d")
                } for b in budgets
            ])
        else:
            return jsonify({"message": "Method not allowed"}), 405

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500