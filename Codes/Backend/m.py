from app import create_app, db
from app.models import users

# Create an app instance
app = create_app()

# Manually push the application context
with app.app_context():
    # Add a new user to the database
    new_user = users(username="testuser", password_hash="hashedpassword", full_name="Test User", email="mm@gmail.com")
    db.session.add(new_user)
    db.session.commit()

    # Query and print all users to verify
    users = users.query.all()
    for user in users:
        print(user.username)  # Should print the username of the created user
