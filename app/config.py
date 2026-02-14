import os

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__)) 
# This gets the absolute path of the directory where this config.py file is located (which is the 'app' folder).

class Config:
    # 1. SECURITY: This is used to sign session cookies. 
    # In production, this should be a long random string from an .env file.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key' # Your Code: Used a hardcoded secret key for simplicity, but this is not secure for production.

    # 2. DATABASE: This tells SQLAlchemy where your database is.
    # We are using SQLite for now (stored in the 'app' folder as 'app.db').
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # 3. PERFORMANCE: This disables a feature we don't need (tracking modifications consumes memory).
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-super-secret-key' # Your Code: Used a hardcoded JWT secret key for simplicity, but this is not secure for production.