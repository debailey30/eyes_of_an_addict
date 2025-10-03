import os

DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'please-set-a-secret'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_SECURE = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Optional: adjust these in environment as needed
PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 days in seconds
