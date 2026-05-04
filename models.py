from flask import Blueprint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, mapped_column, relationship, Mapped
from datetime import datetime

models = Blueprint("models", __name__)


Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(20), default="staff")
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String(100))
    product_image = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float)
    total_price = Column(Float)


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)

    total_amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    order: Mapped["Order"] = relationship()


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    merchant_request_id = Column(String(255))
    checkout_request_id = Column(String(255))
    transaction_code = Column(String(255))
    amount = Column(Float)
    phone_paid = Column(String(20))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone_number = Column(String(20), nullable=False)
    status = Column(String(20), default="PENDING", nullable=False)
    payment_method = Column(String(20), default="MPESA", nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float)