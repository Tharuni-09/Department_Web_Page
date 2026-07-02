from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models.user_model import User
from models.notes_model import Notes
from models.papers_model import Papers
from models.resume_model import Resume
from database import db
from utils.decorators import role_required
from utils.validators import save_file, ALLOWED_DOC_EXTENSIONS
from utils.helpers import get_subject_list, get_semester_list, get_regulation_list

faculty_bp = Blueprint("faculty", __name__)


# ==================== DASHBOARD ====================
@faculty_bp.route("/dashboard")
@role_required("faculty", "hod")
def dashboard():
    user_id = session.get("user_id")
    data = {
        "my_notes": Notes.query.filter_by(uploaded_by=user_id).count(),
        "my_papers": Papers.query.filter_by(uploaded_by=user_id).count(),
        "students": User.query.filter_by(role="student").count(),
        "resumes": Resume.query.count(),
    }
    my_recent_notes = Notes.query.filter_by(uploaded_by=user_id).order_by(Notes.created_at.desc()).limit(5).all()
    my_recent_papers = Papers.query.filter_by(uploaded_by=user_id).order_by(Papers.created_at.desc()).limit(5).all()
    return render_template("faculty/dashboard.html", data=data,
                           recent_notes=my_recent_notes, recent_papers=my_recent_papers)


# ==================== UPLOAD NOTES ====================
@faculty_bp.route("/notes")
@role_required("faculty", "hod")
def my_notes():
    user_id = session.get("user_id")
    notes = Notes.query.filter_by(uploaded_by=user_id).order_by(Notes.created_at.desc()).all()
    return render_template("faculty/notes.html", notes=notes)


@faculty_bp.route("/notes/upload", methods=["GET", "POST"])
@role_required("faculty", "hod")
def upload_note():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Please select a file.", "danger")
            return redirect(url_for("faculty.upload_note"))

        filename = save_file(file, current_app.config["NOTES_FOLDER"], ALLOWED_DOC_EXTENSIONS)
        if not filename:
            flash("Invalid file type. Only PDF/DOCX allowed.", "danger")
            return redirect(url_for("faculty.upload_note"))

        note = Notes(
            title=request.form.get("title", ""),
            description=request.form.get("description", ""),
            filename=filename,
            subject=request.form.get("subject", ""),
            semester=request.form.get("semester", 1, type=int),
            regulation=request.form.get("regulation", ""),
            uploaded_by=session.get("user_id"),
            uploader_role="faculty",
            status="pending"
        )
        db.session.add(note)
        db.session.commit()
        flash("Note uploaded! Waiting for approval. ⏳", "info")
        return redirect(url_for("faculty.my_notes"))

    return render_template("faculty/upload_note.html",
                           subjects=get_subject_list(),
                           semesters=get_semester_list(),
                           regulations=get_regulation_list())


# ==================== UPLOAD PAPERS ====================
@faculty_bp.route("/papers")
@role_required("faculty", "hod")
def my_papers():
    user_id = session.get("user_id")
    papers = Papers.query.filter_by(uploaded_by=user_id).order_by(Papers.created_at.desc()).all()
    return render_template("faculty/papers.html", papers=papers)


@faculty_bp.route("/papers/upload", methods=["GET", "POST"])
@role_required("faculty", "hod")
def upload_paper():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Please select a file.", "danger")
            return redirect(url_for("faculty.upload_paper"))

        filename = save_file(file, current_app.config["PAPERS_FOLDER"], ALLOWED_DOC_EXTENSIONS)
        if not filename:
            flash("Invalid file type. Only PDF/DOCX allowed.", "danger")
            return redirect(url_for("faculty.upload_paper"))

        paper = Papers(
            title=request.form.get("title", ""),
            filename=filename,
            subject=request.form.get("subject", ""),
            semester=request.form.get("semester", 1, type=int),
            regulation=request.form.get("regulation", ""),
            academic_year=request.form.get("academic_year", ""),
            num_pages=request.form.get("num_pages", 0, type=int),
            uploaded_by=session.get("user_id"),
            uploader_role="faculty",
            status="pending"
        )
        db.session.add(paper)
        db.session.commit()
        flash("Paper uploaded! Waiting for approval. ⏳", "info")
        return redirect(url_for("faculty.my_papers"))

    return render_template("faculty/upload_paper.html",
                           subjects=get_subject_list(),
                           semesters=get_semester_list(),
                           regulations=get_regulation_list())


# ==================== VIEW STUDENT RESUMES (PORTFOLIO - READ ONLY) ====================
@faculty_bp.route("/resumes")
@role_required("faculty", "hod")
def view_resumes():
    resumes = Resume.query.all()
    return render_template("faculty/resumes.html", resumes=resumes)


# ==================== PROFILE ====================
@faculty_bp.route("/profile", methods=["GET", "POST"])
@role_required("faculty", "hod")
def profile():
    user = User.query.get(session.get("user_id"))
    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        user.phone = request.form.get("phone", user.phone)
        user.designation = request.form.get("designation", user.designation)
        db.session.commit()
        session["name"] = user.full_name
        flash("Profile updated! ✅", "success")
        return redirect(url_for("faculty.profile"))

    return render_template("faculty/profile.html", user=user)