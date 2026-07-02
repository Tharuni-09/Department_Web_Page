from database import db
from datetime import datetime

class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    package = db.Column(db.String(50), nullable=False)
    eligibility = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    apply_link = db.Column(db.String(500), nullable=True)
    batch_year = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default="active")  # active / closed / upcoming
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", foreign_keys=[created_by], lazy=True)

    def __repr__(self):
        return f"<Placement {self.company} - {self.role}>"