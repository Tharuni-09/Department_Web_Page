from flask import Blueprint, render_template, request
from models.placement_model import Placement
from utils.decorators import login_required

placements_bp = Blueprint("placements", __name__)


@placements_bp.route("/")
@login_required
def view_placements():
    active = Placement.query.filter_by(status="active").order_by(Placement.deadline).all()
    past = Placement.query.filter(Placement.status != "active").order_by(Placement.created_at.desc()).all()
    return render_template("placements/list.html", active=active, past=past)


@placements_bp.route("/<int:id>")
@login_required
def placement_detail(id):
    placement = Placement.query.get_or_404(id)
    return render_template("placements/detail.html", placement=placement)
