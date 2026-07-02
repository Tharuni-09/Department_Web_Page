from database import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    department = db.Column(db.String(100))
    role = db.Column(db.String(20), default="faculty")