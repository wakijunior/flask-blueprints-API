from flask_cors import CORS
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
# from budget.models import models
# from budget.auth import auth  
# from budget.addbudget import addbudget
from budget.auth import jwt, bcrypt
from budget.views import *


load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
# CORS(app, resources={r"/*": {"origins": "*"}})

# app.register_blueprint(models, url_prefix='/')
# app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(addbudget)

# CORS(addbudget, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

if __name__ == '__main__':
    app.run(debug=True)