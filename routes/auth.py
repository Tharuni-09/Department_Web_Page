from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import User
from models.outreach_model import Outreach
from utils.security import verify_password, hash_password
from database import db

auth_bp = Blueprint("auth", __name__)


# ---------------- INDEX / LANDING PAGE ----------------
@auth_bp.route("/")
def index():
    # Show latest outreach events on landing page
    latest_outreach = Outreach.query.filter_by(status="active").order_by(
        Outreach.event_date.desc()
    ).limit(6).all()
    return render_template("index.html", outreach=latest_outreach)


# ---------------- SIGNUP ----------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        phone = request.form.get("phone", "")
        roll_no = request.form.get("roll_no") if role == "student" else None
        
        # Check if username or email exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("auth.signup"))
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("auth.signup"))
            
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=hash_password(password),
            role=role,
            phone=phone,
            roll_no=roll_no,
            status="Active"
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration.", "danger")
            
    return render_template("auth/signup.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for(_get_dashboard_route(session.get("role"))))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user and verify_password(user.password_hash, password):
            if user.status != "Active":
                flash("Your account is inactive. Contact admin.", "danger")
                return redirect(url_for("auth.login"))

            session["user_id"] = user.id
            session["role"] = user.role
            session["name"] = user.full_name
            session["username"] = user.username
            session["department"] = user.department
            session.permanent = True

            flash(f"Welcome back, {user.full_name}! 👋", "success")
            return redirect(url_for(_get_dashboard_route(user.role)))

        flash("Invalid username or password ❌", "danger")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))


def _get_dashboard_route(role):
    routes = {
        "admin": "admin.dashboard",
        "hod": "hod.dashboard",
        "faculty": "faculty.dashboard",
        "student": "student.dashboard",
    }
    return routes.get(role, "auth.login")