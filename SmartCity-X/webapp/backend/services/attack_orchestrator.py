import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..config import PROJECT_ROOT
from ..errors import BackendError


@dataclass(frozen=True)
class AttackDefinition:
    name: str
    attack_script: Path
    detector_script: Path
    soc_script: Path
    working_directory: Path
    telemetry_file: Path
    incident_file: Path


ATTACKS = {
    "traffic": AttackDefinition(
        "TRAFFIC SIGNAL MANIPULATION",
        PROJECT_ROOT / "simulation" / "traffic" / "traffic_signal_attack.py",
        PROJECT_ROOT / "detection" / "traffic_detector.py",
        PROJECT_ROOT / "soc" / "traffic_soc.py",
        PROJECT_ROOT / "simulation" / "traffic",
        PROJECT_ROOT / "simulation" / "traffic" / "attack_telemetry.json",
        PROJECT_ROOT / "soc" / "incident_log.json",
    ),
    "cctv": AttackDefinition(
        "CCTV AUTHENTICATION AND SESSION COMPROMISE",
        PROJECT_ROOT / "simulation" / "cctv" / "cctv_attack.py",
        PROJECT_ROOT / "detection" / "cctv_detector.py",
        PROJECT_ROOT / "soc" / "cctv_soc.py",
        PROJECT_ROOT,
        PROJECT_ROOT / "simulation" / "cctv" / "cctv_telemetry.json",
        PROJECT_ROOT / "soc" / "cctv_incident_log.json",
    ),
    "scada": AttackDefinition(
        "SCADA CONTROL MANIPULATION",
        PROJECT_ROOT / "simulation" / "scada" / "scada_attack.py",
        PROJECT_ROOT / "detection" / "scada_detector.py",
        PROJECT_ROOT / "soc" / "scada_soc.py",
        PROJECT_ROOT / "simulation" / "scada",
        PROJECT_ROOT / "simulation" / "scada" / "scada_telemetry.json",
        PROJECT_ROOT / "soc" / "scada_incident_log.json",
    ),
    "network": AttackDefinition(
        "ROGUE ACCESS POINT",
        PROJECT_ROOT / "simulation" / "network" / "rogue_ap.py",
        PROJECT_ROOT / "detection" / "network_detector.py",
        PROJECT_ROOT / "soc" / "network_soc.py",
        PROJECT_ROOT / "simulation" / "network",
        PROJECT_ROOT / "simulation" / "network" / "network_telemetry.json",
        PROJECT_ROOT / "soc" / "network_incident_log.json",
    ),
    "api": AttackDefinition(
        "UNAUTHORIZED ADMIN API ACCESS",
        PROJECT_ROOT / "simulation" / "api" / "api_attack.py",
        PROJECT_ROOT / "detection" / "api_detector.py",
        PROJECT_ROOT / "soc" / "api_soc.py",
        PROJECT_ROOT / "simulation" / "api",
        PROJECT_ROOT / "simulation" / "api" / "api_telemetry.json",
        PROJECT_ROOT / "soc" / "api_incident_log.json",
    ),
}


def _read_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as data_file:
            return json.load(data_file)
    except (OSError, json.JSONDecodeError) as error:
        raise BackendError(
            f"Expected generated artifact could not be read: {path.name}",
            code="artifact_error",
            status_code=502,
        ) from error


def _run_stage(label: str, script: Path, working_directory: Path) -> dict[str, Any]:
    if not script.is_file():
        raise BackendError(
            f"{label} script is missing",
            code="orchestrator_configuration_error",
            status_code=500,
        )
    try:
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=working_directory,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            timeout=300,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise BackendError(
            f"{label} could not be executed: {error}",
            code="stage_execution_error",
            status_code=502,
        ) from error

    result = {
        "status": "completed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    if completed.returncode:
        raise BackendError(
            f"{label} failed with exit code {completed.returncode}",
            code="stage_failed",
            status_code=502,
        )
    return result


def run_attack(attack_id: str) -> dict[str, Any]:
    definition = ATTACKS.get(attack_id)
    if definition is None:
        raise BackendError(f"Unknown attack '{attack_id}'", code="attack_not_found", status_code=404)

    stages: dict[str, dict[str, Any]] = {}
    stages["attack"] = _run_stage("Attack", definition.attack_script, definition.working_directory)
    telemetry = _read_json(definition.telemetry_file)
    stages["attack"]["telemetry"] = telemetry

    stages["detection"] = _run_stage("Detector", definition.detector_script, PROJECT_ROOT)
    stages["detection"]["telemetry"] = telemetry

    stages["soc"] = _run_stage("SOC", definition.soc_script, PROJECT_ROOT)
    incident = _read_json(definition.incident_file)
    stages["soc"]["incident"] = incident

    final_state = None
    if isinstance(incident, dict):
        final_state = incident.get("status") or incident.get("response") or "SOC_COMPLETED"
    if attack_id == "cctv" and isinstance(telemetry, dict):
        final_state = {
            "authentication": "CONTAINED",
            "session": "REVOKED",
            "stream": "INTERRUPTED",
        }

    return {
        "attack": {
            "id": attack_id,
            "name": definition.name,
            "result": stages["attack"],
        },
        "detection": stages["detection"],
        "soc": stages["soc"],
        "final_state": final_state,
        "execution_status": "completed",
    }
