from app import create_app
from app.extensions import db
from app.models import Restaurant, MenuItem # Ensure these match your model names!
import random

app = create_app()

with app.app_context():
    print("Starting the database seed...")

    # A list of 20 unique restaurants for good search testing
    # Added a fake address to every tuple
    restaurants_data = [
        ("Burger King", "Flame grilled burgers", "123 Flame Way", "burger.jpg"),
        ("Pizza Hut", "Cheesy deep dish pizzas", "456 Crust Ave", "pizza.jpg"),
        ("Sushi Central", "Fresh ocean rolls", "789 Ocean Blvd", "sushi.jpg"),
        ("Taco Fiesta", "Authentic Mexican street food", "101 Salsa St", "taco.jpg"),
        ("Spicy Dragon", "Sichuan Chinese cuisine", "202 Wok Ln", "chinese.jpg"),
        ("Green Leaf Vegan", "100% plant-based bowls", "303 Nature Rd", "vegan.jpg"),
        ("Curry House", "Rich and spicy Indian curries", "404 Spice Cir", "curry.jpg"),
        ("Pasta Bella", "Handmade Italian pasta", "505 Garlic Sq", "pasta.jpg"),
        ("Urban Grill", "Steaks and BBQ", "606 Smoke Dr", "bbq.jpg"),
        ("Sweet Tooth", "Desserts, cakes, and pastries", "707 Sugar Pl", "dessert.jpg"),
        ("Morning Brew", "Artisan coffee and bagels", "808 Bean Ct", "coffee.jpg"),
        ("The Salty Dog", "Fish and chips", "909 Pier Ave", "fish.jpg"),
        ("Pho Real", "Vietnamese noodle soup", "111 Broth Blvd", "pho.jpg"),
        ("Kebab Palace", "Middle Eastern wraps", "222 Skewer St", "kebab.jpg"),
        ("Golden Wok", "Fast and hot stir fry", "333 Noodle Ln", "wok.jpg"),
        ("Crispy Bites", "Fried chicken and sides", "444 Fryer Rd", "chicken.jpg"),
        ("Rustic Oven", "Wood-fired artisan breads", "555 Baker St", "bread.jpg"),
        ("Happy Bowl", "Hawaiian Poke bowls", "666 Island Way", "poke.jpg"),
        ("Magic Spoon", "Gourmet soups and salads", "777 Greens Cir", "soup.jpg"),
        ("Midnight Diner", "Late night comfort food", "888 Moon Dr", "diner.jpg"),
    ]

    # Notice we added 'address' to the unpack variables here:
    for name, desc, address, img in restaurants_data:
        # And we pass address=address into the Restaurant creation
        restaurant = Restaurant(name=name, description=desc, address=address, image_url=img)
        db.session.add(restaurant)
        db.session.flush() 
        
        item1 = MenuItem(
            name=f"Signature {name.split()[0]}", 
            price=round(random.uniform(8.99, 15.99), 2), 
            restaurant_id=restaurant.id
        )
        item2 = MenuItem(
            name="Classic Side", 
            price=round(random.uniform(2.99, 6.99), 2), 
            restaurant_id=restaurant.id
        )
        
        db.session.add_all([item1, item2])

        
    # 3. Commit everything to MySQL permanently
    db.session.commit()
    print("Successfully seeded 20 restaurants and 40 menu items into MySQL!")