from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100), default="Computer Science & Machine Learning")
    role = db.Column(db.String(20), nullable=False)  # admin, hod, faculty, student
    roll_no = db.Column(db.String(50), unique=True, nullable=True)  # students only
    designation = db.Column(db.String(100), nullable=True)  # faculty/hod only
    profile_photo = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default="Active")  # Active / Inactive
    semester = db.Column(db.Integer, nullable=True)  # students only
    batch_year = db.Column(db.String(20), nullable=True)  # students only
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    notes = db.relationship("Notes", backref="uploader", lazy=True, foreign_keys="Notes.uploaded_by")
    papers = db.relationship("Papers", backref="uploader", lazy=True, foreign_keys="Papers.uploaded_by")
    resume = db.relationship("Resume", backref="student", uselist=False, lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
