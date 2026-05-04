from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Blueprint

extensions = Blueprint("extensions", __name__)

bcrypt = Bcrypt()
jwt = JWTManager()