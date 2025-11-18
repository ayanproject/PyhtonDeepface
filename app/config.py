import os
from dotenv import load_dotenv

# Load .env (optional for local)
load_dotenv()

# MySQL credentials from GitHub Secrets
MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_PORT = int(os.getenv("DB_PORT", 3306))
MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
MYSQL_DATABASE = os.getenv("DB_NAME")

# Table name (static)
MYSQL_TABLE = "user_face_entity"

# DeepFace settings
MODEL_NAME = os.getenv("MODEL_NAME", "Facenet")
DISTANCE_METRIC = os.getenv("DISTANCE_METRIC", "cosine")

# Temporary file settings
TMP_FILE_SUFFIX = ".jpg"

# Frontend URL (for CORS)
FRONTEND_URL = os.getenv("FRONTEND_URL")
