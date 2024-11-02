import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'post_pics')
DATABASE = os.path.join(BASE_DIR, 'database.db')
SCHEMA = os.path.join(BASE_DIR, 'schema.sql')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])