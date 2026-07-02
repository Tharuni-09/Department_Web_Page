from database import db
from datetime import datetime

class Notes(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    regulation = db.Column(db.String(50), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    uploader_role = db.Column(db.String(20))  # faculty / student
    status = db.Column(db.String(20), default="pending")  # pending / approved / rejected
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    reject_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approver = db.relationship("User", foreign_keys=[approved_by], lazy=True)

    def __repr__(self):
        return f"<Notes {self.title}>"