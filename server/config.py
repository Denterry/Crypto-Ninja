import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'

    DB_HOST = os.environ.get('DB_HOST', 'db')
    DB_NAME = os.environ.get('DB_NAME', 'crypto_ninja')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
