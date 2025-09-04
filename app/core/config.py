from dotenv import load_dotenv
import os

load_dotenv()

#DB
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


#Keys
SECRET_KEY = os.environ.get("SECRET_KEY")
PAYMENT_SECRET = os.environ.get("PAYMENT_SECRET")
