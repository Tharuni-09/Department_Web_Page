from app import app
from models.user_model import User
from utils.security import hash_password
from database import db

def create_admin():
    with app.app_context():
        existing = User.query.filter_by(username="admin").first()
        if existing:
            print("[OK] Admin already exists.")
            return

        admin = User(
            username="admin",
            email="admin@loyola.edu",
            password_hash=hash_password("admin123"),
            full_name="System Administrator",
            phone="9999999999",
            department="Computer Science & Machine Learning",
            role="admin",
            status="Active"
        )

        db.session.add(admin)
        db.session.commit()

        print("=" * 40)
        print("[OK] Admin Created Successfully")
        print("Username : admin")
        print("Password : admin123")
        print("=" * 40)


if __name__ == "__main__":
    create_admin()