from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models.user_model import User
from models.resume_model import Resume
from database import db
from utils.decorators import role_required, login_required
from utils.validators import save_file, ALLOWED_IMAGE_EXTENSIONS
import json

resume_bp = Blueprint("resume", __name__)


# ==================== STUDENT: CREATE OR EDIT RESUME ====================
@resume_bp.route("/create", methods=["GET", "POST"])
@role_required("student")
def create_resume():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    resume = Resume.query.filter_by(user_id=user_id).first()

    # If resume exists, redirect to edit
    if resume:
        return redirect(url_for("resume.edit_resume"))

    if request.method == "POST":
        resume = Resume(user_id=user_id)
        _update_resume_from_form(resume, request)

        # Handle photo upload
        photo = request.files.get("photo")
        if photo and photo.filename:
            filename = save_file(photo, current_app.config["RESUME_FOLDER"], ALLOWED_IMAGE_EXTENSIONS)
            if filename:
                resume.photo = filename

        db.session.add(resume)
        db.session.commit()
        flash("Resume created successfully! 🎉", "success")
        return redirect(url_for("resume.my_portfolio"))

    return render_template("resume/form.html", resume=None, user=user)


@resume_bp.route("/edit", methods=["GET", "POST"])
@role_required("student")
def edit_resume():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    resume = Resume.query.filter_by(user_id=user_id).first()

    if not resume:
        return redirect(url_for("resume.create_resume"))

    if request.method == "POST":
        _update_resume_from_form(resume, request)

        # Handle photo upload
        photo = request.files.get("photo")
        if photo and photo.filename:
            filename = save_file(photo, current_app.config["RESUME_FOLDER"], ALLOWED_IMAGE_EXTENSIONS)
            if filename:
                resume.photo = filename

        db.session.commit()
        flash("Resume updated! ✅", "success")
        return redirect(url_for("resume.my_portfolio"))

    return render_template("resume/form.html", resume=resume, user=user)


# ==================== STUDENT: VIEW OWN PORTFOLIO ====================
@resume_bp.route("/portfolio")
@role_required("student")
def my_portfolio():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    resume = Resume.query.filter_by(user_id=user_id).first()
    if not resume:
        flash("Please create your resume first.", "info")
        return redirect(url_for("resume.create_resume"))

    return render_template("resume/portfolio.html", resume=resume, user=user)


# ==================== VIEW ANY STUDENT PORTFOLIO (Faculty/HOD/Admin) ====================
@resume_bp.route("/view/<int:user_id>")
@login_required
def view_portfolio(user_id):
    role = session.get("role")
    if role == "student" and user_id != session.get("user_id"):
        flash("Access denied.", "danger")
        return redirect(url_for("student.dashboard"))

    user = User.query.get_or_404(user_id)
    resume = Resume.query.filter_by(user_id=user_id).first()
    if not resume:
        flash("This student hasn't created a resume yet.", "info")
        return redirect(request.referrer or url_for("auth.login"))

    return render_template("resume/portfolio.html", resume=resume, user=user)


def _update_resume_from_form(resume, req):
    """Update resume object from form data."""
    resume.about = req.form.get("about", "")
    resume.career_objective = req.form.get("career_objective", "")
    resume.contact_email = req.form.get("contact_email", "")
    resume.contact_phone = req.form.get("contact_phone", "")
    resume.linkedin = req.form.get("linkedin", "")
    resume.github = req.form.get("github", "")
    resume.portfolio_url = req.form.get("portfolio_url", "")

    # Parse JSON array fields from form
    resume.education = _parse_json_field(req, "education")
    resume.skills = _parse_json_field(req, "skills")
    resume.projects = _parse_json_field(req, "projects")
    resume.certifications = _parse_json_field(req, "certifications")
    resume.achievements = _parse_json_field(req, "achievements")
    resume.internships = _parse_json_field(req, "internships")


def _parse_json_field(req, field_name):
    """Parse a JSON field from form data."""
    raw = req.form.get(field_name, "[]")
    try:
        data = json.loads(raw) if raw else []
        return json.dumps(data)
    except (json.JSONDecodeError, TypeError):
        return "[]"
