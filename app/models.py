"""
This Model represents a User in the system. 
It includes fields for username, email, password, and other relevant information. 
The User model is used for authentication and authorization purposes, 
allowing users to log in and access protected resources within the application. 
It also includes methods for password hashing and verification to ensure secure handling of user credentials.
"""


# app/models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash #password hashing utilities
from app.extensions import db  # <--- IMPORT FROM EXTENSIONS

# --- User & Authentication Models ---

class User(db.Model):
    __tablename__ = 'users' # Your Code: Relied on SQLAlchemy to guess the table name (it would likely guess user)
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True) # Added index for speed
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False) # Increased length for stronger hashes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # This allows us to access user.addresses
    addresses = db.relationship('Address', backref='user', lazy=True) #backref allows us to access address.user, 
    # lazy=True means addresses are loaded only when we access user.addresses, not every time we load a user.

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True) # ADDED PRIMARY KEY
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    street = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False) # Renamed 'zip' (reserved keyword)


# --- Restaurant & Menu Models ---

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(255))
    
    # Relationships
    # cascade="all, delete-orphan" means if you delete a Restaurant, 
    # its menu items are automatically deleted too.
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True, cascade="all, delete-orphan") #backref allows us to access menu_item.restaurant
    #lazy=True means the menu items are loaded only when we access restaurant.menu_items, not every time we load a restaurant.

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    # CHANGED Float to Numeric for money precision
    price = db.Column(db.Numeric(10, 2), nullable=False) 
    is_active = db.Column(db.Boolean, default=True) # Good to soft-delete items
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)



# app/models.py

# ... (Previous imports and User/Restaurant models) ...

# --- Order Management Models ---

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    
    # Who placed the order?
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Which restaurant is it from?
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    # Status: pending, preparing, delivered, cancelled
    status = db.Column(db.String(20), default='pending')
    
    # Total Price (Cached here for speed)
    total_price = db.Column(db.Numeric(10, 2), default=0.00)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # This creates a link so we can access order.items later
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    
    # Link to the Order Header
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    # Link to the original Menu Item (so we know it was a Whopper)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    
    # Snapshot of the data at the moment of purchase
    price_at_order = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(120), nullable=False) # Store name too in case MenuItem is deleted