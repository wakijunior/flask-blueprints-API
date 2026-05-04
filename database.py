from flask import Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

database = Blueprint("database", __name__)

load_dotenv()

DATABASE_URL = os.getenv("db_url")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()