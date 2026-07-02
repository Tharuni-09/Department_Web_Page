import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "loyola-erp-secret-key-2024")
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "loyola_erp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "connect_args": {"check_same_thread": False},
    }

    # Uploads
    UPLOAD_FOLDER = os.path.join(BASEDIR, "uploads")
    NOTES_FOLDER = os.path.join(UPLOAD_FOLDER, "notes")
    PAPERS_FOLDER = os.path.join(UPLOAD_FOLDER, "papers")
    OUTREACH_FOLDER = os.path.join(UPLOAD_FOLDER, "outreach")
    RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, "resumes")
    PROFILE_FOLDER = os.path.join(UPLOAD_FOLDER, "profiles")
    PPT_FOLDER = os.path.join(UPLOAD_FOLDER, "ppt")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    ALLOWED_DOC_EXTENSIONS = {"pdf", "docx", "doc"}
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_ALL_EXTENSIONS = ALLOWED_DOC_EXTENSIONS | ALLOWED_IMAGE_EXTENSIONS

    # Gemini AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Session
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours