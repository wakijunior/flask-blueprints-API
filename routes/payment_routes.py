from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Payment, Order
from database import get_db
from mpesa import make_stk_push
from generatePdf import generate_pdf

payments = Blueprint("payments", __name__)



@payments.route("/stk-push", methods=["POST"])
def stk_push():

    data = request.get_json()
    order_id = data.get("order_id")
    phone = data.get("phone_number")

    if not order_id or not phone:
        return jsonify({"error": "Missing required fields"}), 400

    with get_db() as db:

        order = db.query(Order).filter_by(id=order_id).first()

        if not order:
            return jsonify({"error": "Order not found"}), 404

        if order.status == "PAID":
            return jsonify({"error": "Order already paid"}), 400

        # ✅ Use backend amount
        amount = order.total_amount

        stk_payload = {
            "phone_number": phone,
            "amount": amount,
            "order_id": order_id
        }

        stk_response = make_stk_push(stk_payload)

        payment = Payment(
            order_id=order.id,
            merchant_request_id=stk_response.get("MerchantRequestID"),
            checkout_request_id=stk_response.get("CheckoutRequestID"),
            amount=amount,
            phone_paid=phone,
            status="PENDING"
        )

        db.add(payment)
        db.commit()

    return jsonify(stk_response)

@payments.route("/stk-call-back", methods=["POST"])
def stk_callback():

    data = request.get_json()

    try:
        stk_callback = data["Body"]["stkCallback"]

        merchant_request_id = stk_callback.get("MerchantRequestID")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode")

        with get_db() as db:

            payment = db.query(Payment).filter_by(
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id
            ).first()

            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            # ✅ Prevent double processing
            if payment.status == "SUCCESS":
                return jsonify({"message": "Already processed"}), 200

            order = db.query(Order).filter_by(id=payment.order_id).first()

            if result_code == 0:

                callback_items = stk_callback["CallbackMetadata"]["Item"]

                metadata = {
                    item["Name"]: item.get("Value")
                    for item in callback_items
                }

                payment.transaction_code = metadata.get("MpesaReceiptNumber")
                payment.amount = metadata.get("Amount")
                payment.phone_paid = str(metadata.get("PhoneNumber"))
                payment.status = "SUCCESS"

                # ✅ UPDATE ORDER
                order.status = "PAID"

                # ✅ REDUCE STOCK
                for item in order.items:
                    item.product.quantity -= item.quantity

                # ✅ GENERATE RECEIPT
                receipt_text = f"""
                Payment Receipt

                Transaction Code: {payment.transaction_code}
                Amount: {payment.amount}
                Phone: {payment.phone_paid}
                Status: SUCCESS
                """

                generate_pdf(
                    receipt_text,
                    f"{payment.transaction_code}.pdf"
                )

            else:
                payment.status = "FAILED"
                order.status = "FAILED"

            db.commit()

        return jsonify({"message": "Callback processed"}), 200

    except Exception as e:
        print("Callback error:", str(e))
        return jsonify({"error": "Callback failed"}), 500

@payments.route("/mpesa-payments", methods=["GET"])
@jwt_required()
def get_payments():

    with get_db() as db:

        payments = db.query(Payment).all()

        return jsonify([
            {
                "id": p.id,
                "order_id": p.order_id,  # ✅ FIXED
                "transaction_code": p.transaction_code,
                "amount": p.amount,
                "phone_paid": p.phone_paid,
                "status": p.status,
                "created_at": p.created_at
            }
            for p in payments
        ])