from flask import Blueprint, current_app, jsonify, send_from_directory

from ..config import PROJECT_ROOT
from ..schemas import success_response


cctv_bp = Blueprint("cctv", __name__, url_prefix="/api/cctv")


def _service():
    return current_app.extensions["cctv_service"]


@cctv_bp.get("")
def list_cctv():
    return jsonify(success_response(_service().list_cameras()))


@cctv_bp.get("/<camera_id>")
def get_cctv(camera_id: str):
    return jsonify(success_response(_service().get_camera(camera_id)))


@cctv_bp.get("/<camera_id>/video")
def get_video(camera_id: str):
    camera = _service().get_camera(camera_id)
    if camera["stream"] != "ACTIVE":
        return jsonify({"status": "error", "error": {"code": "stream_interrupted", "message": "CCTV stream interrupted"}}), 503
    return send_from_directory(PROJECT_ROOT / "simulation" / "cctv" / "videos", camera["video"])


@cctv_bp.post("/<camera_id>/attack")
def attack_cctv(camera_id: str):
    return jsonify(success_response(_service().attack(camera_id), status="attack_applied"))


@cctv_bp.post("/<camera_id>/soc")
def soc_cctv(camera_id: str):
    return jsonify(success_response(_service().contain(camera_id), status="contained"))


@cctv_bp.post("/<camera_id>/reset")
def reset_cctv(camera_id: str):
    return jsonify(success_response(_service().reset(camera_id), status="recovered"))
