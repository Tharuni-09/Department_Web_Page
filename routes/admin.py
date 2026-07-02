from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models.user_model import User
from models.notes_model import Notes
from models.papers_model import Papers
from models.outreach_model import Outreach, OutreachImage
from models.placement_model import Placement
from models.resume_model import Resume
from models.notification_model import Notification
from database import db
from utils.decorators import role_required
from utils.security import hash_password
from utils.validators import save_file, delete_file, ALLOWED_IMAGE_EXTENSIONS
from utils.helpers import get_subject_list, get_semester_list, get_regulation_list, get_category_list
from datetime import datetime

admin_bp = Blueprint("admin", __name__)


# ==================== DASHBOARD ====================
@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    data = {
        "faculty": User.query.filter_by(role="faculty").count(),
        "hod": User.query.filter_by(role="hod").count(),
        "students": User.query.filter_by(role="student").count(),
        "notes": Notes.query.count(),
        "papers": Papers.query.count(),
        "placements": Placement.query.count(),
        "outreach": Outreach.query.count(),
        "resumes": Resume.query.count(),
        "pending_notes": Notes.query.filter_by(status="pending").count(),
        "pending_papers": Papers.query.filter_by(status="pending").count(),
    }
    recent_notes = Notes.query.order_by(Notes.created_at.desc()).limit(5).all()
    recent_papers = Papers.query.order_by(Papers.created_at.desc()).limit(5).all()
    recent_outreach = Outreach.query.order_by(Outreach.created_at.desc()).limit(5).all()
    notifications = Notification.query.filter_by(
        user_id=session.get("user_id"), is_read=False
    ).order_by(Notification.created_at.desc()).limit(10).all()

    return render_template("admin/dashboard.html", data=data,
                           recent_notes=recent_notes, recent_papers=recent_papers,
                           recent_outreach=recent_outreach, notifications=notifications)


# ==================== FACULTY MANAGEMENT ====================
@admin_bp.route("/faculty")
@role_required("admin")
def faculty_list():
    faculty = User.query.filter(User.role.in_(["faculty", "hod"])).order_by(User.full_name).all()
    return render_template("admin/faculty.html", faculty=faculty)


@admin_bp.route("/faculty/add", methods=["GET", "POST"])
@role_required("admin")
def add_faculty():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists!", "danger")
            return redirect(url_for("admin.add_faculty"))

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(request.form.get("password", "faculty123")),
            full_name=request.form.get("full_name", ""),
            phone=request.form.get("phone", ""),
            department=request.form.get("department", "Computer Science & Machine Learning"),
            role=request.form.get("role", "faculty"),
            designation=request.form.get("designation", ""),
            status="Active"
        )
        db.session.add(user)
        db.session.commit()
        flash("Faculty added successfully! ✅", "success")
        return redirect(url_for("admin.faculty_list"))

    return render_template("admin/faculty_form.html", edit=None)


@admin_bp.route("/faculty/edit/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def edit_faculty(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        user.email = request.form.get("email", user.email)
        user.phone = request.form.get("phone", user.phone)
        user.designation = request.form.get("designation", user.designation)
        user.department = request.form.get("department", user.department)
        user.role = request.form.get("role", user.role)
        user.status = request.form.get("status", user.status)

        new_pass = request.form.get("password", "").strip()
        if new_pass:
            user.password_hash = hash_password(new_pass)

        db.session.commit()
        flash("Faculty updated! ✅", "success")
        return redirect(url_for("admin.faculty_list"))

    return render_template("admin/faculty_form.html", edit=user)


@admin_bp.route("/faculty/delete/<int:id>")
@role_required("admin")
def delete_faculty(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("Faculty deleted.", "info")
    return redirect(url_for("admin.faculty_list"))


# ==================== STUDENT MANAGEMENT ====================
@admin_bp.route("/students")
@role_required("admin")
def student_list():
    students = User.query.filter_by(role="student").order_by(User.full_name).all()
    return render_template("admin/students.html", students=students)


@admin_bp.route("/students/add", methods=["GET", "POST"])
@role_required("admin")
def add_student():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        roll_no = request.form.get("roll_no", "").strip()

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists!", "danger")
            return redirect(url_for("admin.add_student"))

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(request.form.get("password", "student123")),
            full_name=request.form.get("full_name", ""),
            phone=request.form.get("phone", ""),
            department=request.form.get("department", "Computer Science & Machine Learning"),
            role="student",
            roll_no=roll_no,
            semester=request.form.get("semester", type=int),
            batch_year=request.form.get("batch_year", ""),
            status="Active"
        )
        db.session.add(user)
        db.session.commit()
        flash("Student added successfully! ✅", "success")
        return redirect(url_for("admin.student_list"))

    return render_template("admin/student_form.html", edit=None,
                           semesters=get_semester_list())


@admin_bp.route("/students/edit/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def edit_student(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        user.email = request.form.get("email", user.email)
        user.phone = request.form.get("phone", user.phone)
        user.roll_no = request.form.get("roll_no", user.roll_no)
        user.semester = request.form.get("semester", type=int)
        user.batch_year = request.form.get("batch_year", user.batch_year)
        user.status = request.form.get("status", user.status)

        new_pass = request.form.get("password", "").strip()
        if new_pass:
            user.password_hash = hash_password(new_pass)

        db.session.commit()
        flash("Student updated! ✅", "success")
        return redirect(url_for("admin.student_list"))

    return render_template("admin/student_form.html", edit=user,
                           semesters=get_semester_list())


@admin_bp.route("/students/delete/<int:id>")
@role_required("admin")
def delete_student(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("Student deleted.", "info")
    return redirect(url_for("admin.student_list"))


# ==================== NOTES MANAGEMENT ====================
@admin_bp.route("/notes")
@role_required("admin")
def notes_list():
    status_filter = request.args.get("status", "all")
    query = Notes.query.order_by(Notes.created_at.desc())
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    notes = query.all()
    return render_template("admin/notes.html", notes=notes, current_filter=status_filter)


@admin_bp.route("/notes/approve/<int:id>")
@role_required("admin")
def approve_note(id):
    note = Notes.query.get_or_404(id)
    note.status = "approved"
    note.approved_by = session.get("user_id")
    note.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Note approved! ✅", "success")
    return redirect(url_for("admin.notes_list"))


@admin_bp.route("/notes/reject/<int:id>", methods=["POST"])
@role_required("admin")
def reject_note(id):
    note = Notes.query.get_or_404(id)
    note.status = "rejected"
    note.reject_reason = request.form.get("reason", "")
    note.approved_by = session.get("user_id")
    note.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Note rejected.", "info")
    return redirect(url_for("admin.notes_list"))


@admin_bp.route("/notes/delete/<int:id>")
@role_required("admin")
def delete_note(id):
    note = Notes.query.get_or_404(id)
    delete_file(note.filename, current_app.config["NOTES_FOLDER"])
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("admin.notes_list"))


# ==================== PAPERS MANAGEMENT ====================
@admin_bp.route("/papers")
@role_required("admin")
def papers_list():
    status_filter = request.args.get("status", "all")
    query = Papers.query.order_by(Papers.created_at.desc())
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    papers = query.all()
    return render_template("admin/papers.html", papers=papers, current_filter=status_filter)


@admin_bp.route("/papers/approve/<int:id>")
@role_required("admin")
def approve_paper(id):
    paper = Papers.query.get_or_404(id)
    paper.status = "approved"
    paper.approved_by = session.get("user_id")
    paper.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Paper approved! ✅", "success")
    return redirect(url_for("admin.papers_list"))


@admin_bp.route("/papers/reject/<int:id>", methods=["POST"])
@role_required("admin")
def reject_paper(id):
    paper = Papers.query.get_or_404(id)
    paper.status = "rejected"
    paper.reject_reason = request.form.get("reason", "")
    paper.approved_by = session.get("user_id")
    paper.approved_at = datetime.utcnow()
    db.session.commit()
    flash("Paper rejected.", "info")
    return redirect(url_for("admin.papers_list"))


@admin_bp.route("/papers/delete/<int:id>")
@role_required("admin")
def delete_paper(id):
    paper = Papers.query.get_or_404(id)
    delete_file(paper.filename, current_app.config["PAPERS_FOLDER"])
    db.session.delete(paper)
    db.session.commit()
    flash("Paper deleted.", "info")
    return redirect(url_for("admin.papers_list"))


# ==================== OUTREACH MANAGEMENT ====================
@admin_bp.route("/outreach")
@role_required("admin")
def outreach_list():
    events = Outreach.query.order_by(Outreach.event_date.desc()).all()
    return render_template("admin/outreach.html", outreach=events,
                           categories=get_category_list())


@admin_bp.route("/outreach/add", methods=["GET", "POST"])
@role_required("admin")
def add_outreach():
    if request.method == "POST":
        event = Outreach(
            title=request.form.get("title", ""),
            description=request.form.get("description", ""),
            event_date=datetime.strptime(request.form.get("event_date", ""), "%Y-%m-%d").date(),
            location=request.form.get("location", ""),
            category=request.form.get("category", "event"),
            status="active",
            created_by=session.get("user_id")
        )
        db.session.add(event)
        db.session.flush()  # Get event.id

        # Handle multiple image uploads
        images = request.files.getlist("images")
        for img in images:
            if img and img.filename:
                filename = save_file(img, current_app.config["OUTREACH_FOLDER"], ALLOWED_IMAGE_EXTENSIONS)
                if filename:
                    caption = ""
                    outreach_img = OutreachImage(
                        outreach_id=event.id,
                        filename=filename,
                        caption=caption
                    )
                    db.session.add(outreach_img)

        db.session.commit()
        flash("Outreach event added! ✅", "success")
        return redirect(url_for("admin.outreach_list"))

    return render_template("admin/outreach_form.html", edit=None,
                           categories=get_category_list())


@admin_bp.route("/outreach/edit/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def edit_outreach(id):
    event = Outreach.query.get_or_404(id)
    if request.method == "POST":
        event.title = request.form.get("title", event.title)
        event.description = request.form.get("description", event.description)
        event.event_date = datetime.strptime(request.form.get("event_date", ""), "%Y-%m-%d").date()
        event.location = request.form.get("location", event.location)
        event.category = request.form.get("category", event.category)
        event.status = request.form.get("status", event.status)

        # Handle new image uploads
        images = request.files.getlist("images")
        for img in images:
            if img and img.filename:
                filename = save_file(img, current_app.config["OUTREACH_FOLDER"], ALLOWED_IMAGE_EXTENSIONS)
                if filename:
                    outreach_img = OutreachImage(
                        outreach_id=event.id,
                        filename=filename,
                        caption=""
                    )
                    db.session.add(outreach_img)

        db.session.commit()
        flash("Outreach event updated! ✅", "success")
        return redirect(url_for("admin.outreach_list"))

    return render_template("admin/outreach_form.html", edit=event,
                           categories=get_category_list())


@admin_bp.route("/outreach/delete/<int:id>")
@role_required("admin")
def delete_outreach(id):
    event = Outreach.query.get_or_404(id)
    for img in event.images:
        delete_file(img.filename, current_app.config["OUTREACH_FOLDER"])
    db.session.delete(event)
    db.session.commit()
    flash("Outreach event deleted.", "info")
    return redirect(url_for("admin.outreach_list"))


@admin_bp.route("/outreach/image/delete/<int:id>")
@role_required("admin")
def delete_outreach_image(id):
    img = OutreachImage.query.get_or_404(id)
    event_id = img.outreach_id
    delete_file(img.filename, current_app.config["OUTREACH_FOLDER"])
    db.session.delete(img)
    db.session.commit()
    flash("Image removed.", "info")
    return redirect(url_for("admin.edit_outreach", id=event_id))


# ==================== PLACEMENTS MANAGEMENT ====================
@admin_bp.route("/placements")
@role_required("admin")
def placements_list():
    placements = Placement.query.order_by(Placement.created_at.desc()).all()
    return render_template("admin/placements.html", placements=placements)


@admin_bp.route("/placements/add", methods=["GET", "POST"])
@role_required("admin")
def add_placement():
    if request.method == "POST":
        deadline = request.form.get("deadline", "")
        p = Placement(
            company=request.form.get("company", ""),
            role=request.form.get("role", ""),
            package=request.form.get("package", ""),
            eligibility=request.form.get("eligibility", ""),
            description=request.form.get("description", ""),
            deadline=datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None,
            apply_link=request.form.get("apply_link", ""),
            batch_year=request.form.get("batch_year", ""),
            status="active",
            created_by=session.get("user_id")
        )
        db.session.add(p)
        db.session.commit()
        flash("Placement drive added! ✅", "success")
        return redirect(url_for("admin.placements_list"))

    return render_template("admin/placement_form.html", edit=None)


@admin_bp.route("/placements/edit/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def edit_placement(id):
    p = Placement.query.get_or_404(id)
    if request.method == "POST":
        p.company = request.form.get("company", p.company)
        p.role = request.form.get("role", p.role)
        p.package = request.form.get("package", p.package)
        p.eligibility = request.form.get("eligibility", p.eligibility)
        p.description = request.form.get("description", p.description)
        deadline = request.form.get("deadline", "")
        p.deadline = datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else p.deadline
        p.apply_link = request.form.get("apply_link", p.apply_link)
        p.batch_year = request.form.get("batch_year", p.batch_year)
        p.status = request.form.get("status", p.status)
        db.session.commit()
        flash("Placement updated! ✅", "success")
        return redirect(url_for("admin.placements_list"))

    return render_template("admin/placement_form.html", edit=p)


@admin_bp.route("/placements/delete/<int:id>")
@role_required("admin")
def delete_placement(id):
    p = Placement.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash("Placement deleted.", "info")
    return redirect(url_for("admin.placements_list"))


# ==================== RESUME MANAGEMENT ====================
@admin_bp.route("/resumes")
@role_required("admin")
def resume_list():
    resumes = Resume.query.all()
    return render_template("admin/resumes.html", resumes=resumes)


# ==================== SETTINGS ====================
@admin_bp.route("/settings")
@role_required("admin")
def settings():
    return render_template("admin/settings.html")