# from flask import Flask
# from flask_jwt_extended import JWTManager
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# import os

# load_dotenv()

# db = SQLAlchemy()
# jwt = JWTManager()
# bcrypt = Bcrypt()

# def create_app():
#     app = Flask(__name__)

#     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     db.init_app(app)
#     jwt.init_app(app)
#     bcrypt.init_app(app)
#     # CORS(app, resources={r"/*": {"origins": "*"}})
#     CORS.init_app(app)

#     from .models import models
#     from .auth import auth  
#     from .addbudget import addbudget
   
#     app.register_blueprint(models, url_prefix='/')
#     app.register_blueprint(auth, url_prefix='/')
#     app.register_blueprint(addbudget, url_prefix='/')


#     return app







