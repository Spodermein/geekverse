from database import SessionLocal
from models import Category

def seed_categories():
    db = SessionLocal()

    categories = [
        "Tech",
        "Gaming",
        "Dinosaurs & Comics",
        "Gym & Sports",
        "Others"
    ]

    for name in categories:
        exists = db.query(Category).filter(Category.name == name).first()
        if not exists:
            db.add(Category(name=name))

    db.commit()
    db.close()
    print("✅ Categories seeded successfully")

if __name__ == "__main__":
    seed_categories()
