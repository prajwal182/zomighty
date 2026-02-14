# app/__init__.py
from flask import Flask
from app.extensions import db
from app.config import Config 

def create_app(config_class=Config):  # <--- 1. The "Machine" starts here
    app = Flask(__name__)             # <--- 2. Create a blank car chassis
    app.config.from_object(config_class) # <--- 3. Install the specific parts (settings)

    # Initialize Flask extensions
    db.init_app(app)                  # <--- 4. Plug in the engine (Database)

    # Register Blueprints (We will do this later)
    # from app.api.auth import auth_bp
    # app.register_blueprint(auth_bp)
    
    return app                        # <--- 5. Deliver the finished car