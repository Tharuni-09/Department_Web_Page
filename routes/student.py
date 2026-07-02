from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import User
from models.notes_model import Notes
from models.papers_model import Papers
from models.placement_model import Placement
from models.resume_model import Resume
from database import db
from utils.decorators import role_required

student_bp = Blueprint("student", __name__)


# ==================== DASHBOARD ====================
@student_bp.route("/dashboard")
@role_required("student")
def dashboard():
    user_id = session.get("user_id")
    data = {
        "notes": Notes.query.filter_by(status="approved").count(),
        "papers": Papers.query.filter_by(status="approved").count(),
        "placements": Placement.query.filter_by(status="active").count(),
        "has_resume": Resume.query.filter_by(user_id=user_id).first() is not None,
    }
    recent_notes = Notes.query.filter_by(status="approved").order_by(Notes.created_at.desc()).limit(5).all()
    active_placements = Placement.query.filter_by(status="active").order_by(Placement.created_at.desc()).limit(5).all()
    return render_template("student/dashboard.html", data=data,
                           recent_notes=recent_notes, active_placements=active_placements)


# ==================== VIEW APPROVED NOTES ====================
@student_bp.route("/notes")
@role_required("student")
def view_notes():
    subject = request.args.get("subject", "")
    semester = request.args.get("semester", "")
    query = Notes.query.filter_by(status="approved")
    if subject:
        query = query.filter_by(subject=subject)
    if semester:
        query = query.filter_by(semester=int(semester))
    notes = query.order_by(Notes.created_at.desc()).all()
    return render_template("student/notes.html", notes=notes)


# ==================== VIEW APPROVED PAPERS ====================
@student_bp.route("/papers")
@role_required("student")
def view_papers():
    subject = request.args.get("subject", "")
    semester = request.args.get("semester", "")
    query = Papers.query.filter_by(status="approved")
    if subject:
        query = query.filter_by(subject=subject)
    if semester:
        query = query.filter_by(semester=int(semester))
    papers = query.order_by(Papers.created_at.desc()).all()
    return render_template("student/papers.html", papers=papers)


# ==================== PLACEMENTS ====================
@student_bp.route("/placements")
@role_required("student")
def placements():
    active = Placement.query.filter_by(status="active").order_by(Placement.deadline).all()
    past = Placement.query.filter(Placement.status != "active").order_by(Placement.created_at.desc()).all()
    return render_template("student/placements.html", active=active, past=past)


# ==================== PROFILE ====================
@student_bp.route("/profile", methods=["GET", "POST"])
@role_required("student")
def profile():
    user = User.query.get(session.get("user_id"))
    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        user.phone = request.form.get("phone", user.phone)
        db.session.commit()
        session["name"] = user.full_name
        flash("Profile updated! ✅", "success")
        return redirect(url_for("student.profile"))

    return render_template("student/profile.html", user=user)