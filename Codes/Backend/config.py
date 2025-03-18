import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-quran-memorization-app'
    DEBUG = True
    
    # Database configuration
    DB_HOST = 'localhost'
    DB_USER = 'root'  # Replace with your MySQL username
    DB_PASSWORD = ''  # Replace with your MySQL password
    DB_NAME = 'quran_memorization_db'  # Replace with your database name