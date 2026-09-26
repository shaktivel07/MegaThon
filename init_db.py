
from app import app
from models import db,User
from werkzeug.security import generate_password_hash
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="Shakthi").first():
        db.session.add(User(username="Shakthi",password=generate_password_hash("Shakthi123"),is_admin=True))
        db.session.commit()
print("Database initialized.")
