from flask import Blueprint, render_template, send_from_directory, current_app
from models.outreach_model import Outreach
from utils.decorators import login_required

outreach_bp = Blueprint("outreach", __name__)


# ==================== PUBLIC GALLERY ====================
@outreach_bp.route("/")
def gallery():
    events = Outreach.query.filter_by(status="active").order_by(Outreach.event_date.desc()).all()
    return render_template("outreach/gallery.html", events=events)


@outreach_bp.route("/event/<int:id>")
def event_detail(id):
    event = Outreach.query.get_or_404(id)
    return render_template("outreach/detail.html", event=event)


# ==================== SERVE IMAGES ====================
@outreach_bp.route("/image/<filename>")
def serve_image(filename):
    return send_from_directory(current_app.config["OUTREACH_FOLDER"], filename)
