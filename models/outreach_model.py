from database import db
from datetime import datetime

class Outreach(db.Model):
    __tablename__ = "outreach"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), default="event")  # workshop/seminar/hackathon/guest_lecture/event
    status = db.Column(db.String(20), default="active")  # active / inactive
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship("OutreachImage", backref="event", lazy=True, cascade="all, delete-orphan")
    creator = db.relationship("User", foreign_keys=[created_by], lazy=True)

    def __repr__(self):
        return f"<Outreach {self.title}>"


class OutreachImage(db.Model):
    __tablename__ = "outreach_images"

    id = db.Column(db.Integer, primary_key=True)
    outreach_id = db.Column(db.Integer, db.ForeignKey("outreach.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<OutreachImage {self.filename}>"