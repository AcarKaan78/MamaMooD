import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask configuration
SECRET_KEY = 'mamamood-secret-key-2025'
DATABASE = os.path.join(BASE_DIR, 'mamamood.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'videos')
DEBUG = True
