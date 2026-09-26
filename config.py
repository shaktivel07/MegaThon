
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR=Path(__file__).resolve().parent
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","tsrm-secret-key")
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL") or f"sqlite:///{BASE_DIR/'tsrm.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
