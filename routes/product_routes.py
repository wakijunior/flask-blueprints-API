from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Product, User
from database import get_db
from decorators import role_required

products = Blueprint("products", __name__)

@products.route("/products", methods=["POST"])
@jwt_required()
@role_required("admin")  # 🔥 enable this
def create_product():

    data = request.get_json()

    product_name = data.get("product_name")
    product_image = data.get("product_image")
    quantity = data.get("quantity")
    price = data.get("price")

    # ✅ Validation
    if not product_name:
        return jsonify({"error": "Product name required"}), 400

    try:
        quantity = int(quantity)
        price = float(price)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid quantity or price"}), 400

    if quantity < 0 or price < 0:
        return jsonify({"error": "Values must be positive"}), 400

    user_id = get_jwt_identity()  # ✅ assume JWT stores user_id

    with get_db() as db:

        product = Product(
            user_id=user_id,
            product_name=product_name,
            product_image=product_image,
            quantity=quantity,
            price=price
        )

        db.add(product)
        db.commit()

        return jsonify({
            "message": "Product created",
            "product_id": product.id
        }), 201
        
@products.route("/products", methods=["GET"])
@jwt_required()
def get_products():

    with get_db() as db:

        products = db.query(Product).all()

        return jsonify([
            {
                "id": p.id,
                "product_name": p.product_name,
                "product_image": p.product_image,
                "quantity": p.quantity,
                "price": p.price
            }
            for p in products
        ])