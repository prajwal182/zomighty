# app/api/restaurants.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Restaurant, MenuItem
from flask_jwt_extended import jwt_required

# Create the Blueprint
restaurants_bp = Blueprint('restaurants', __name__)

# --- ROUTES GO HERE ---
@restaurants_bp.route('/', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    data = []
    for restaurant in restaurants:
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "description": restaurant.description,
            "address": restaurant.address,
            "image_url": restaurant.image_url,
            "menu_items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "price": item.price
                } for item in restaurant.menu_items
            ]
        }
        data.append(restaurant_data)
    return jsonify(data), 200

# create a restaurant
@restaurants_bp.route('/', methods=['POST'])
@jwt_required() # This means you must be logged in to create a restaurant
def create_restaurant():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or Content-Type header missing"}), 400
    name = data.get("name")
    address = data.get("address")
    description = data.get("description")

    if not name or not address:
        return jsonify({"error": "Missing required fields: name and address"}), 400
    
    new_restaurant = Restaurant(
            name=name, 
            address=address, 
            description=description, 
            image_url="image_url"
        )
    
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({"message": "Restaurant created successfully", "id": new_restaurant.id}), 201


# the restaurant menu items route
# app/api/restaurants.py

# ... existing imports ...

@restaurants_bp.route('/<int:restaurant_id>/items', methods=['POST'])
@jwt_required()
def add_menu_item(restaurant_id):
    # 1. Check if restaurant exists
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    data = request.get_json()
    
    # 2. Validation
    if not data.get('name') or not data.get('price'):
        return jsonify({"error": "Name and Price are required"}), 400
        
    # 3. Create Item
    new_item = MenuItem(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        restaurant_id=restaurant.id # Linking it here
    )
    
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({"message": "Menu item added", "id": new_item.id}), 201

