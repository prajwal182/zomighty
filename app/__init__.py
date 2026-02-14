# app/__init__.py
from flask import Flask
from app.extensions import db, jwt
from app.config import Config 

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

    
    return app                        # <--- 5. Deliver the finished car