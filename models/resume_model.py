from database import db
from datetime import datetime
import json

class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)  # 1 student = 1 resume
    photo = db.Column(db.String(255), nullable=True)
    about = db.Column(db.Text, nullable=True)
    career_objective = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)  # JSON string
    skills = db.Column(db.Text, nullable=True)  # JSON string
    projects = db.Column(db.Text, nullable=True)  # JSON string
    certifications = db.Column(db.Text, nullable=True)  # JSON string
    achievements = db.Column(db.Text, nullable=True)  # JSON string
    internships = db.Column(db.Text, nullable=True)  # JSON string
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    github = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Helper methods to get/set JSON fields
    def get_education(self):
        try:
            return json.loads(self.education) if self.education else []
        except:
            return []

    def set_education(self, data):
        self.education = json.dumps(data)

    def get_skills(self):
        try:
            return json.loads(self.skills) if self.skills else []
        except:
            return []

    def set_skills(self, data):
        self.skills = json.dumps(data)

    def get_projects(self):
        try:
            return json.loads(self.projects) if self.projects else []
        except:
            return []

    def set_projects(self, data):
        self.projects = json.dumps(data)

    def get_certifications(self):
        try:
            return json.loads(self.certifications) if self.certifications else []
        except:
            return []

    def set_certifications(self, data):
        self.certifications = json.dumps(data)

    def get_achievements(self):
        try:
            return json.loads(self.achievements) if self.achievements else []
        except:
            return []

    def set_achievements(self, data):
        self.achievements = json.dumps(data)

    def get_internships(self):
        try:
            return json.loads(self.internships) if self.internships else []
        except:
            return []

    def set_internships(self, data):
        self.internships = json.dumps(data)

    def __repr__(self):
        return f"<Resume user_id={self.user_id}>"
