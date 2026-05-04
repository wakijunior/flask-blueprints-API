from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models import Order, OrderItem, Product
from routes.payment_routes import stk_push

orders = Blueprint("orders", __name__)


@orders.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()

    items = data.get('items', [])
    phone = data.get('phone_number')

    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    if not phone:
        return jsonify({"error": "Phone number required"}), 400

    user_id = get_jwt_identity()

    with get_db() as db:

        total = 0
        order_items = []

        # ✅ 1. Validate items & calculate total securely
        for item in items:
            product = db.query(Product).filter_by(id=item['id']).first()

            if not product:
                return jsonify({"error": f"Product {item['id']} not found"}), 404

            if product.quantity < item['qty']:
                return jsonify({
                    "error": f"Not enough stock for {product.product_name}"
                }), 400

            # ✅ USE DB PRICE (NOT FRONTEND)
            price = product.price
            total += price * item['qty']

            order_items.append({
                "product": product,
                "quantity": item['qty'],
                "price": price
            })

        # ✅ 2. Create order (not committed yet)
        order = Order(
            user_id=user_id,
            phone_number=phone,
            total_amount=total,
            status="PENDING"
        )
        db.add(order)
        db.flush()  # get order.id without committing

        # ✅ 3. Save items
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                unit_price=item["price"]
            )
            db.add(order_item)

        # ✅ 4. Commit everything once
        db.commit()

    # ✅ 5. Call STK AFTER commit
    stk_push(phone, total, order.id)

    return jsonify({
        "message": "Order created",
        "order_id": order.id,
        "total": total
    }), 201