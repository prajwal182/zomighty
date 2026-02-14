from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User

# 1. Create the Blueprint (Think of this as a "Plugin")
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # 2. validation: Did they send JSON?
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or Content-Type header missing"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # 3. Validation: Are fields missing?
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # 4. Check for existing users
    # (Clean Code Tip: Check logic separately for better error messages)
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409 # 409 = Conflict
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    # 5. Create and Save
    new_user = User(username=username, email=email)
    new_user.set_password(password) # Using the method we wrote in models.py
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201