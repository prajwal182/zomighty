"""This module initializes and configures Flask extensions for the Zomighty application."""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager # For handling JSON Web Tokens (JWT) for authentication

db = SQLAlchemy()
jwt = JWTManager() # Initialize JWTManager, but we will call jwt.init_app(app) in create_app() to link it to our Flask app.