import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__)) 
# This gets the absolute path of the directory where this config.py file is located (which is the 'app' folder).

class Config:
    # 1. SECURITY: This is used to sign session cookies. 
    # In production, this should be a long random string from an .env file.
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key' # Your Code: Used a hardcoded secret key for simplicity, but this is not secure for production.
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')


    # 2. DATABASE: This tells SQLAlchemy where your database is.
    # We are using SQLite for now (stored in the 'app' folder as 'app.db').
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app.db'))
    # Note: The above line first checks for DATABASE_URL in the environment variables. If it doesn't find it, 
    # it defaults to using a SQLite database located at '../app.db' relative to this config.py file. 
    # This allows for easy switching between a local SQLite database and a production database (like MySQL) by just setting the DATABASE_URL environment variable.



    # 3. PERFORMANCE: This disables a feature we don't need (tracking modifications consumes memory).
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 4. JWT CONFIG: This is the secret key for signing JWT tokens.
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-super-secret-key' # Your Code: Used a hardcoded JWT secret key for simplicity, but this is not secure for production.
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1) # Tokens will expire after 1 day