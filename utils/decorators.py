from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(f):
    """Require user to be logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Require user to have one of the specified roles. Admin always passes."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login first.", "warning")
                return redirect(url_for("auth.login"))

            user_role = session.get("role")

            # Admin has access to everything
            if user_role == "admin":
                return f(*args, **kwargs)

            if user_role not in roles:
                flash("Access Denied ❌", "danger")
                return redirect(url_for("auth.login"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator