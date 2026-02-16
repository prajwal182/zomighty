# app/__init__.py
from flask import Flask
from app.extensions import db, jwt
from app.config import Config 
from app.api.restaurants import restaurants_bp
from app.api.orders import orders_bp
from app.errors import register_error_handlers

def create_app(config_class=Config):  # <--- 1. The "Machine" starts here
    app = Flask(__name__)             # <--- 2. Create a blank car chassis
    app.config.from_object(config_class) # <--- 3. Install the specific parts (settings)

    # Initialize Flask extensions
    db.init_app(app)                  # <--- 4. Plug in the engine (Database)
    jwt.init_app(app)                 # <--- Plug in the JWT system for authentication


    # --- REGISTER BLUEPRINTS HERE ---
    from app.api.auth import auth_bp
    
    # url_prefix means all routes in auth.py will start with /api/auth
    # So the route is now: POST /api/auth/register
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Register the restaurants blueprint
    app.register_blueprint(restaurants_bp, url_prefix='/api/restaurants')

    # Register the orders blueprint
    app.register_blueprint(orders_bp, url_prefix='/api/orders')  

    # --- NEW: Register Error Handlers ---
    # from app.errors import register_error_handlers
    register_error_handlers(app)


    return app                        # <--- 5. Deliver the finished car