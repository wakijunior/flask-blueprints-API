from datetime import datetime
from flask import Blueprint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey


# models = Blueprint('models', __name__)

class Base(DeclarativeBase):
    pass


# ------------------ USER ------------------
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationship
    budgets = relationship("Budget", back_populates="user")


# ------------------ BUDGET ------------------
class Budget(Base):
    __tablename__ = "mybudget"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationship
    user = relationship("User", back_populates="budgets")