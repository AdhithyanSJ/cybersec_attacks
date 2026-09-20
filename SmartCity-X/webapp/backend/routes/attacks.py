from flask import Blueprint, jsonify

from ..schemas import success_response
from ..services.attack_orchestrator import run_attack


attacks_bp = Blueprint("attacks", __name__, url_prefix="/api/attacks")


def _launch(attack_id: str):
    return jsonify(success_response(run_attack(attack_id), status="completed"))


@attacks_bp.post("/traffic")
def launch_traffic():
    return _launch("traffic")


@attacks_bp.post("/cctv")
def launch_cctv():
    return _launch("cctv")


@attacks_bp.post("/scada")
def launch_scada():
    return _launch("scada")


@attacks_bp.post("/network")
def launch_network():
    return _launch("network")


@attacks_bp.post("/api")
def launch_api():
    return _launch("api")
