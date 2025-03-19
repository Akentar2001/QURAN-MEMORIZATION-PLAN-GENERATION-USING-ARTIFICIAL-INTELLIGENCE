from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Create an SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

def get_db_connection():
    try:
        # Establish a connection
        connection = engine.connect()
        print("Connection")
        return connection
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL Database: {e}")
        return None

get_db_connection()