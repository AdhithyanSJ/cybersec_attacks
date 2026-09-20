import json
import os
from datetime import datetime

import requests


SERVER = "http://127.0.0.1:5000"
TELEMETRY_FILE = os.path.join("simulation", "cctv", "cctv_telemetry.json")
INCIDENT_LOG = os.path.join("soc", "cctv_incident_log.json")


def main() -> int:
    if not os.path.exists(TELEMETRY_FILE):
        print("[ERROR] CCTV telemetry not found.")
        return 1

    with open(TELEMETRY_FILE, encoding="utf-8") as telemetry_file:
        telemetry = json.load(telemetry_file)
    camera_id = telemetry.get("camera_id")
    if not camera_id:
        print("[ERROR] CCTV telemetry has no camera ID.")
        return 1

    try:
        response = requests.post(f"{SERVER}/api/cctv/{camera_id}/soc", timeout=5)
        response.raise_for_status()
        result = response.json()["data"]
    except requests.RequestException as error:
        print(f"[ERROR] CCTV containment failed: {error}")
        return 1

    incident = result["incident"]
    os.makedirs(os.path.dirname(INCIDENT_LOG), exist_ok=True)
    with open(INCIDENT_LOG, "w", encoding="utf-8") as incident_file:
        json.dump(incident, incident_file, indent=4)

    print("=" * 60)
    print("               CCTV SOC CONTAINMENT")
    print("=" * 60)
    print("[RESPONSE] Attacker session revoked.")
    print("[RESPONSE] Unauthorized access contained.")
    print("[RESPONSE] CCTV stream remains interrupted.")
    print(f"Response: {result['response']}")
    print(f"Incident Log: {INCIDENT_LOG}")
    print(f"Completed at: {datetime.now().isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
