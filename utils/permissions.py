from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if "role" not in session:
                return redirect(url_for("auth.login"))

            if session.get("role") != role and session.get("role") != "admin":
                flash("Access Denied ❌", "danger")
                return redirect(url_for("auth.login"))

            return func(*args, **kwargs)

        return wrapper
    return decorator