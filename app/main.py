from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import bcrypt
import os
from app import config
from app.utils import save_bytes_to_tempfile
from app.verifier import verify_faces_by_path

app = FastAPI(title="Face Verification Service")

# ---- CORS FIX ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://red-plant-01033d700.3.azurestaticapps.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_user_from_mysql(voter_id: str):
    conn = None
    try:
        conn = pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        with conn.cursor() as cur:
            # Fetch ALL users because bcrypt cannot search directly
            sql = f"SELECT face_image, encrypted_voter_id, encrypted_secret_pin FROM `{config.MYSQL_TABLE}`"
            cur.execute(sql)
            rows = cur.fetchall()

            # Find the matching user by bcrypt comparing encrypted voter_id
            for row in rows:
                if bcrypt.checkpw(voter_id.encode(), row["encrypted_voter_id"].encode()):
                    return row  # ✅ Correct user found

            return None  # ❌ No matching user

    finally:
        if conn:
            conn.close()


@app.post("/verify")
async def verify_face(
    voter_id: str = Form(...),
    secret_pin: str = Form(...),
    probe_image: UploadFile = File(...)
):
    user = fetch_user_from_mysql(voter_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check credentials
    if not bcrypt.checkpw(voter_id.encode(), user["encrypted_voter_id"].encode()):
        return {"verified": False, "reason": "Wrong Voter ID"}

    if not bcrypt.checkpw(secret_pin.encode(), user["encrypted_secret_pin"].encode()):
        return {"verified": False, "reason": "Wrong Secret PIN"}

    # Save stored + probe images temporarily
    stored_path = save_bytes_to_tempfile(user["face_image"])
    probe_path = save_bytes_to_tempfile(await probe_image.read())

    result = verify_faces_by_path(probe_path, stored_path, config.MODEL_NAME, config.DISTANCE_METRIC)

    os.remove(stored_path)
    os.remove(probe_path)

    return {
        "verified": bool(result.get("verified", False)),
        "distance": result.get("distance")
    }
