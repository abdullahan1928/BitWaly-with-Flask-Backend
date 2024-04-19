import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key_here'
    FLASK_RUN_PORT = 3000
    MONGO_URI = os.getenv('MONGO_URI')
    CLIENT_DEV_URL = os.getenv('CLIENT_DEV_URL')
    CLIENT_PROD_URL = os.getenv('CLIENT_PROD_URL')
