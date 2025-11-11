import os
from dotenv import load_dotenv

# load .env if present (optional)
load_dotenv()

# MySQL defaults based on your Spring properties (override via envvars if needed)
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "4321")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "Voteonn")

# Table defaults
MYSQL_TABLE = os.getenv("MYSQL_TABLE", "user_face_entity")
# We will look for any BLOB-like column in the returned row (faceImage / face_image / faceimage ...)

# Local test directory (put {voter_id}.jpg here to bypass DB during dev)
LOCAL_TEST_DIR = os.getenv("LOCAL_TEST_DIR", "./test_data")

# DeepFace settings
MODEL_NAME = os.getenv("MODEL_NAME", "Facenet")
DISTANCE_METRIC = os.getenv("DISTANCE_METRIC", "cosine")

# Other
TMP_FILE_SUFFIX = os.getenv("TMP_FILE_SUFFIX", ".jpg")
