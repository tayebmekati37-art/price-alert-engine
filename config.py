import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///alerts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings (Gmail SMTP)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or MAIL_USERNAME

    # Alert check interval (seconds)
    CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 30))

    # Cooldown period (seconds) before sending another notification for same alert
    NOTIFICATION_COOLDOWN = int(os.environ.get('NOTIFICATION_COOLDOWN', 3600))  # 1 hour
