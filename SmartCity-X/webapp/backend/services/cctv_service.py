import json
import secrets
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any

from ..config import PROJECT_ROOT
from ..errors import BackendError


TELEMETRY_FILE = PROJECT_ROOT / "simulation" / "cctv" / "cctv_telemetry.json"
INCIDENT_FILE = PROJECT_ROOT / "soc" / "cctv_incident_log.json"
CONTROLLED_CREDENTIALS = (("admin", "123456"), ("admin", "password"), ("admin", "admin"))


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class CCTVService:
    """Authoritative in-process CCTV state used by the orchestration backend."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._cameras: dict[str, dict[str, Any]] = {
            camera_id: {
                "id": camera_id,
                "location": location,
                "video": f"{camera_id}.mp4",
                "status": "ONLINE",
                "authentication": "AUTHORIZED",
                "session": "LEGITIMATE",
                "stream": "ACTIVE",
                "active_token": None,
            }
            for camera_id, location in (
                ("CAM-01", "Main Street Intersection"),
                ("CAM-02", "City Center"),
                ("CAM-03", "Public Parking Area"),
            )
        }
        self._attack_state: dict[str, Any] = {
            "active": False,
            "camera": None,
            "authentication_failures": 0,
            "successful_login": False,
            "unauthorized_session": False,
            "legitimate_session_terminated": False,
            "stream_interrupted": False,
            "attacker_token": None,
        }
        self._telemetry: dict[str, Any] | None = self._read_json(TELEMETRY_FILE)
        self._incident: dict[str, Any] | None = self._read_json(INCIDENT_FILE)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            with path.open(encoding="utf-8") as data_file:
                value = json.load(data_file)
            return value if isinstance(value, dict) else None
        except (OSError, json.JSONDecodeError):
            return None

    @staticmethod
    def _write_json(path: Path, value: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as data_file:
            json.dump(value, data_file, indent=4)

    def _camera(self, camera_id: str) -> dict[str, Any]:
        camera = self._cameras.get(camera_id)
        if camera is None:
            raise BackendError(f"Camera '{camera_id}' was not found", code="camera_not_found", status_code=404)
        return camera

    def list_cameras(self) -> dict[str, Any]:
        with self._lock:
            return {
                "cameras": deepcopy(list(self._cameras.values())),
                "attack": deepcopy(self._attack_state),
                "telemetry": deepcopy(self._telemetry),
                "incident": deepcopy(self._incident),
            }

    def get_camera(self, camera_id: str) -> dict[str, Any]:
        with self._lock:
            return deepcopy(self._camera(camera_id))

    def get_telemetry(self) -> dict[str, Any] | None:
        with self._lock:
            return deepcopy(self._telemetry)

    def attack(self, camera_id: str) -> dict[str, Any]:
        with self._lock:
            camera = self._camera(camera_id)
            failures = len(CONTROLLED_CREDENTIALS) - 1
            attacker_token = f"ATTACKER-{secrets.token_hex(8)}"
            camera.update(
                authentication="COMPROMISED",
                session="UNAUTHORIZED",
                stream="INTERRUPTED",
                active_token=attacker_token,
            )
            self._attack_state.update(
                active=True,
                camera=camera_id,
                authentication_failures=failures,
                successful_login=True,
                unauthorized_session=True,
                legitimate_session_terminated=True,
                stream_interrupted=True,
                attacker_token=attacker_token,
            )
            self._telemetry = {
                "timestamp": _timestamp(),
                "target": "CCTV",
                "camera_id": camera_id,
                "camera_location": camera["location"],
                "authentication_failures": failures,
                "successful_unauthorized_login": True,
                "unauthorized_session": True,
                "attacker_session": attacker_token,
                "legitimate_session_terminated": True,
                "stream_interrupted": True,
                "attack": "CCTV AUTHENTICATION AND SESSION COMPROMISE",
                "impact": "UNAUTHORIZED CAMERA ACCESS",
                "authoritative_state": {
                    "authentication": camera["authentication"],
                    "session": camera["session"],
                    "stream": camera["stream"],
                },
            }
            self._write_json(TELEMETRY_FILE, self._telemetry)
            return {"camera": deepcopy(camera), "attack": deepcopy(self._attack_state), "telemetry": deepcopy(self._telemetry)}

    def contain(self, camera_id: str) -> dict[str, Any]:
        with self._lock:
            camera = self._camera(camera_id)
            if not self._attack_state["active"] or self._attack_state["camera"] != camera_id:
                raise BackendError("No active CCTV attack exists for this camera", code="no_active_attack", status_code=409)
            camera.update(authentication="CONTAINED", session="REVOKED", active_token=None, stream="INTERRUPTED")
            incident = {
                "incident_id": f"SCX-CCTV-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(3).upper()}",
                "timestamp": _timestamp(),
                "threat": "CCTV AUTHENTICATION AND SESSION COMPROMISE",
                "severity": "HIGH",
                "camera_id": camera_id,
                "camera_location": camera["location"],
                "authentication_failures": self._attack_state["authentication_failures"],
                "unauthorized_session": True,
                "legitimate_session_terminated": True,
                "stream_interrupted": True,
                "response": "CONTAINMENT",
                "status": "CONTAINED",
                "response_type": "SIMULATED_SOC_RESPONSE",
                "actions": ["ATTACKER_SESSION_REVOKED", "UNAUTHORIZED_ACCESS_CONTAINED"],
            }
            self._incident = incident
            self._attack_state["active"] = False
            self._write_json(INCIDENT_FILE, incident)
            return {"camera": deepcopy(camera), "response": "CONTAINMENT", "incident": deepcopy(incident)}

    def reset(self, camera_id: str) -> dict[str, Any]:
        with self._lock:
            camera = self._camera(camera_id)
            camera.update(
                status="ONLINE",
                authentication="AUTHORIZED",
                session="LEGITIMATE",
                stream="ACTIVE",
                active_token=None,
            )
            self._attack_state = {
                "active": False,
                "camera": None,
                "authentication_failures": 0,
                "successful_login": False,
                "unauthorized_session": False,
                "legitimate_session_terminated": False,
                "stream_interrupted": False,
                "attacker_token": None,
            }
            return {"camera": deepcopy(camera), "response": "MANUAL_RECOVERY"}
