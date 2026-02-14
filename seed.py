# seed.py
from app import create_app, db
from app.models import User, Restaurant, MenuItem

app = create_app() #create_app() is the factory function that sets up our Flask app with all configurations and extensions.

def seed_data():
    """Populates the database with dummy data for testing."""
    with app.app_context():
        # 1. Reset the Database (Drop all tables and recreate them)
        # WARNING: This deletes all data! Only use in Dev.
        print("🗑️  Dropping old data...")
        db.drop_all()
        print("🔨 Creating new tables...")
        db.create_all()

        # 2. Create a Dummy User
        print("👤 Creating Users...")
        user1 = User(username="prajwal", email="prajwal@test.com")
        user1.set_password("password123") # Hashing the password
        
        db.session.add(user1)

        # 3. Create a Restaurant
        print("🍕 Creating Restaurants...")
        rest1 = Restaurant(
            name="Pizza Palace",
            description="Best pizza in Nashik",
            address="College Road, Nashik",
            image_url="https://placehold.co/600x400"
        )
        
        db.session.add(rest1)
        
        # 4. Commit to save User & Restaurant so they get IDs
        db.session.commit() 

        # 5. Create Menu Items (Linked to the Restaurant)
        print("🍔 Creating Menu Items...")
        item1 = MenuItem(
            name="Margherita Pizza",
            description="Classic cheese and tomato",
            price=250.00,
            restaurant=rest1  # SQLAlchemy magic: We pass the object, not the ID!
        )
        
        item2 = MenuItem(
            name="Garlic Bread",
            description="Buttery garlic goodness",
            price=120.50,
            restaurant=rest1
        )

        db.session.add_all([item1, item2])
        
        # 6. Final Commit
        db.session.commit()
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_data()