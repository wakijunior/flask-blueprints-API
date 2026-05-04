from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
import os

# ROUTES
from routes.auth_routes import auth
from routes.product_routes import products
from routes.analytics_routes import analytics
from routes.admin_routes import admin
from routes.payment_routes import payments
from routes.sales_routes import sales
from routes.user_routes import users
from routes.upload_routes import uploads
from routes.reports_routes import reports
from database import database, engine
from models import models, Base
from extensions import extensions, bcrypt, jwt
from routes.orders_routes import orders

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("jwt_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# INITIALIZE EXTENSIONS
bcrypt.init_app(app)
jwt.init_app(app)

CORS(
    app,
    origins=["http://127.0.0.1:5500"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
)

Base.metadata.create_all(engine)

# REGISTER BLUEPRINTS
app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(analytics)
app.register_blueprint(admin)
app.register_blueprint(payments)
app.register_blueprint(sales)
app.register_blueprint(users)
app.register_blueprint(uploads)
app.register_blueprint(reports)
app.register_blueprint(database)
app.register_blueprint(models)
app.register_blueprint(extensions)
app.register_blueprint(orders)


@app.route("/")
def home():
    return "Welcome"

if __name__ == "__main__":
    app.run(debug=True)