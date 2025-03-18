from app import db
from app.models import User, Student

new_user = User(username="testuser", password_hash="hashedpassword", full_name="Test User")
db.session.add(new_user)
db.session.commit()

print(User.query.all())  # Should return the created user
