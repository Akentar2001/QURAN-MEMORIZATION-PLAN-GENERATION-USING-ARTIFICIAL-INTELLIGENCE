import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None