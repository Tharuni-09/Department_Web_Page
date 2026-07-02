from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory, current_app
from models.notes_model import Notes
from database import db
from utils.decorators import login_required, role_required
from utils.validators import save_file, ALLOWED_DOC_EXTENSIONS
from utils.helpers import get_subject_list, get_semester_list, get_regulation_list

notes_bp = Blueprint("notes", __name__)


# ==================== VIEW APPROVED NOTES ====================
@notes_bp.route("/")
@login_required
def view_notes():
    subject = request.args.get("subject", "")
    semester = request.args.get("semester", "")

    role = session.get("role")
    if role in ("admin", "hod"):
        query = Notes.query
    else:
        query = Notes.query.filter_by(status="approved")

    if subject:
        query = query.filter_by(subject=subject)
    if semester:
        query = query.filter_by(semester=int(semester))

    notes = query.order_by(Notes.created_at.desc()).all()
    return render_template("notes/list.html", notes=notes,
                           subjects=get_subject_list(),
                           semesters=get_semester_list())


# ==================== UPLOAD NOTES ====================
@notes_bp.route("/upload", methods=["GET", "POST"])
@role_required("faculty", "hod", "student")
def upload_note():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Please select a file.", "danger")
            return redirect(url_for("notes.upload_note"))

        filename = save_file(file, current_app.config["NOTES_FOLDER"], ALLOWED_DOC_EXTENSIONS)
        if not filename:
            flash("Invalid file type. Only PDF/DOCX allowed.", "danger")
            return redirect(url_for("notes.upload_note"))

        note = Notes(
            title=request.form.get("title", ""),
            description=request.form.get("description", ""),
            filename=filename,
            subject=request.form.get("subject", ""),
            semester=request.form.get("semester", 1, type=int),
            regulation=request.form.get("regulation", ""),
            uploaded_by=session.get("user_id"),
            uploader_role=session.get("role"),
            status="pending"
        )
        db.session.add(note)
        db.session.commit()
        flash("Notes uploaded! Waiting for approval. ⏳", "info")
        return redirect(url_for("notes.view_notes"))

    return render_template("notes/upload.html",
                           subjects=get_subject_list(),
                           semesters=get_semester_list(),
                           regulations=get_regulation_list())


# ==================== DOWNLOAD ====================
@notes_bp.route("/download/<filename>")
@login_required
def download_note(filename):
    return send_from_directory(current_app.config["NOTES_FOLDER"], filename,
                               as_attachment=True)