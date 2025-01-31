# Configuration file for CareConnect AI
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'careconnect_secret_key'
    GEMINI_API_KEY = 'AIzaSyAh78MT0xRVUPqg7NouDTBV_8YBtJ1BGdc'
    DATABASE_URI = 'sqlite:///database/careconnect.db'
