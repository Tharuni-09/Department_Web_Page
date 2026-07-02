from database import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), default="info")  # info / success / warning / danger
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.id} for user {self.user_id}>"
