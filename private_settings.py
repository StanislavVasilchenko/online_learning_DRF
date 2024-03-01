import os

from dotenv import load_dotenv

load_dotenv()

DJANGO_KEY = os.getenv('DJANGO_KEY')

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")


BROKER_URL = os.getenv("BROKER_URL")
RESULT_BACKEND = os.getenv("RESULT_BACKEND")

HOST = os.getenv("EMAIL_HOST")
HOST_USER = os.getenv("HOST_USER")
HOST_PASSWORD = os.getenv("HOST_PASSWORD")