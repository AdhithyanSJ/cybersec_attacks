from flask import Blueprint, jsonify

from ..schemas import success_response
from ..services.scada_service import reset_breaker_state


scada_bp = Blueprint("scada", __name__, url_prefix="/api/scada")


@scada_bp.post("/reset")
def reset_scada():
    return jsonify(success_response(reset_breaker_state()))
