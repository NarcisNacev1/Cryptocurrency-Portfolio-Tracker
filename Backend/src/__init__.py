from flask import Flask
from Backend.src.extensions import db, migrate
from Backend.src.routes.transaction import transaction_routes
from Backend.src.routes.portfolio import portfolio_routes
from Backend.src.routes.transaction import transaction_routes
from flask_jwt_extended import JWTManager
from flask_session import Session
from Backend.src.routes.auth import auth_routes
from flask_cors import CORS
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swawggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Cryptocurrency Portfolio Tracker"}
    )

    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config.from_object("Backend.src.config.config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    Session(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(transaction_routes)
    app.register_blueprint(portfolio_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(swawggerui_blueprint, url_prefix=SWAGGER_URL)

    return app