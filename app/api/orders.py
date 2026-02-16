# app/api/orders.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Order, OrderItem, MenuItem, Restaurant
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def place_order():
    # 1. Get User
    current_user_id = get_jwt_identity()
    
    # 2. Get Data
    data = request.get_json()
    restaurant_id = data.get('restaurant_id')
    items_data = data.get('items') # Expecting list: [{"menu_item_id": 1, "quantity": 2}]

    if not restaurant_id or not items_data:
        return jsonify({"error": "Missing restaurant_id or items"}), 400

    # 3. Validation: Does Restaurant Exist?
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # --- CALCULATE & BUILD ---
    total_price = 0
    order_items_objects = []

    for item in items_data:
        # Fetch the real food item from DB
        menu_item = MenuItem.query.get(item['menu_item_id'])
        
        if not menu_item:
            return jsonify({"error": f"Item {item['menu_item_id']} not found"}), 404
            
        # Security Check: Don't let them order a Pizza from a Burger King order
        if menu_item.restaurant_id != restaurant.id:
            return jsonify({"error": "Item does not belong to this restaurant"}), 400

        # Calculate Cost
        qty = item['quantity']
        if qty < 1:
            return jsonify({"error": "Quantity must be positive"}), 400
            
        item_total = menu_item.price * qty
        total_price += item_total
        
        # Create the Snapshot (The Receipt Line)
        order_item = OrderItem(
            menu_item_id=menu_item.id,
            price_at_order=menu_item.price, # FREEZING THE PRICE
            quantity=qty,
            item_name=menu_item.name
        )
        order_items_objects.append(order_item)

    # 4. Create the Order Header
    new_order = Order(
        user_id=current_user_id,
        restaurant_id=restaurant.id,
        total_price=total_price,
        status='pending'
    )
    
    # 5. Link Items to Order
    # We add the order to the session first so it gets an ID
    db.session.add(new_order)
    db.session.flush() # This generates the ID for new_order without committing yet
    
    for obj in order_items_objects:
        obj.order_id = new_order.id # Link them
        db.session.add(obj)
        
    # 6. Final Commit (Atomic Transaction)
    db.session.commit()
    
    return jsonify({
        "message": "Order placed successfully", 
        "order_id": new_order.id,
        "total": float(total_price)
    }), 201


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_orders():
    current_user_id = get_jwt_identity()
    
    # 1. Fetch Orders for THIS user only
    # order_by(desc) puts the newest orders at the top
    orders = Order.query.filter_by(user_id=current_user_id)\
        .order_by(Order.created_at.desc()).all()
    
    data = []
    
    for order in orders:
        # 2. Build the "Inner" List (The Items)
        items_data = []
        for item in order.items:
            items_data.append({
                "name": item.item_name,
                "quantity": item.quantity,
                "price": str(item.price_at_order)
            })
            
        # 3. Build the "Outer" Object (The Order)
        data.append({
            "id": order.id,
            "restaurant_id": order.restaurant_id,
            "status": order.status,
            "total_price": str(order.total_price),
            "date": order.created_at.isoformat(),
            "items": items_data # <--- Nesting the list here
        })
        
    return jsonify(data), 200


@orders_bp.route('/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_order_status(order_id):
    # 1. Get the Data
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['pending', 'preparing', 'delivered', 'cancelled']
    
    if new_status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    # 2. Find the Order
    order = Order.query.get_or_404(order_id)
    
    # 3. Update & Save
    order.status = new_status
    db.session.commit()
    
    return jsonify({"message": f"Order status updated to {new_status}"}), 200