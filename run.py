from app import create_app
from app.extensions import db

app = create_app()

# --- ADD THIS BLOCK ---
# This forces the app to create the tables automatically before starting
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
# ----------------------

if __name__ == '__main__':
    app.run(debug=True)
    