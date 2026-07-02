from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import User
from models.notes_model import Notes
from models.papers_model import Papers
from models.resume_model import Resume
from database import db
from utils.decorators import role_required
from datetime import datetime

hod_bp = Blueprint("hod", __name__)


# ==================== DASHBOARD ====================
@hod_bp.route("/dashboard")
@role_required("hod")
def dashboard():
    data = {
        "faculty": User.query.filter_by(role="faculty").count(),
        "students": User.query.filter_by(role="student").count(),
        "notes": Notes.query.count(),
        "papers": Papers.query.count(),
        "pending_notes": Notes.query.filter_by(status="pending").count(),
        "pending_papers": Papers.query.filter_by(status="pending").count(),
        "resumes": Resume.query.count(),
    }
    return render_template("hod/dashboard.html", data=data)


# ==================== FACULTY VIEW ====================
@hod_bp.route("/faculty")
@role_required("hod")
def faculty_view():
    faculty = User.query.filter_by(role="faculty").order_by(User.full_name).all()
    return render_template("hod/faculty.html", faculty=faculty)


# ==================== STUDENT REPORTS ====================
@hod_bp.route("/students")
@role_required("hod")
def student_reports():
    students = User.query.filter_by(role="student").order_by(User.full_name).all()
    return render_template("hod/students.html", students=students)


# ==================== APPROVE NOTES ====================
@hod_bp.route("/notes")
@role_required("hod")
def notes_list():
    status_filter = request.args.get("status", "pending")
    query = Notes.query.order_by(Notes.created_at.desc())
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    notes = query.all()
    return render_template("hod/notes.html", notes=notes, current_filter=status_filter)


@hod_bp.route("/notes/approve/<int:id>")
@role_required("hod")
def approve_note(id):
    note = Notes.query.get_or_404(id)
    note.status = "approved"
    note.approved_by = session.get("user_id")
    note.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Note approved! ✅", "success")
    return redirect(url_for("hod.notes_list"))


@hod_bp.route("/notes/reject/<int:id>", methods=["POST"])
@role_required("hod")
def reject_note(id):
    note = Notes.query.get_or_404(id)
    note.status = "rejected"
    note.reject_reason = request.form.get("reason", "")
    note.approved_by = session.get("user_id")
    note.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Note rejected.", "info")
    return redirect(url_for("hod.notes_list"))


# ==================== APPROVE PAPERS ====================
@hod_bp.route("/papers")
@role_required("hod")
def papers_list():
    status_filter = request.args.get("status", "pending")
    query = Papers.query.order_by(Papers.created_at.desc())
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    papers = query.all()
    return render_template("hod/papers.html", papers=papers, current_filter=status_filter)


@hod_bp.route("/papers/approve/<int:id>")
@role_required("hod")
def approve_paper(id):
    paper = Papers.query.get_or_404(id)
    paper.status = "approved"
    paper.approved_by = session.get("user_id")
    paper.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Paper approved! ✅", "success")
    return redirect(url_for("hod.papers_list"))


@hod_bp.route("/papers/reject/<int:id>", methods=["POST"])
@role_required("hod")
def reject_paper(id):
    paper = Papers.query.get_or_404(id)
    paper.status = "rejected"
    paper.reject_reason = request.form.get("reason", "")
    paper.approved_by = session.get("user_id")
    paper.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Paper rejected.", "info")
    return redirect(url_for("hod.papers_list"))


# ==================== RESUME VIEW (PORTFOLIO) ====================
@hod_bp.route("/resumes")
@role_required("hod")
def resume_list():
    resumes = Resume.query.all()
    return render_template("hod/resumes.html", resumes=resumes)