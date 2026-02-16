from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity 
# For creating JWT tokens and protecting routes


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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or content-type header missing"}), 400
    
    
    # username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # 1. Find the user
    user = User.query.filter_by(email=email).first()

    # 2. check if user exists and password is correct
    if user and user.check_password(password):
        # 3. create the token
        # identity=user.id means "This token belongs to user #5"
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "message":"Login Successfully",
            "access_token":access_token,
            "user": {"id":user.id, "username":user.username}
        }), 200

    # 4. If we get here, it means login failed
    return jsonify({"error": "Invalid email or password"}), 401

# create an endpoint that returns the currently logged-in user's profile. 
# If you try to access this without a token, the server will block you.
@auth_bp.route('/me', methods=['GET'])
# The Bouner (Blocks request if no token or invalid token)
@jwt_required() # This decorator protects the route, only allowing access with a valid JWT token
def get_current_user():
    # 1. Get the user ID from the token
    current_user_id = get_jwt_identity()

    # 2. Fetch the user from the database
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # 3. Return the data
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "joined_at": user.created_at.isoformat()
    }), 200

