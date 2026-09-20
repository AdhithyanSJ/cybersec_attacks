import json
import os
from datetime import datetime

import requests


SERVER = "http://127.0.0.1:5000"
CAMERA_ID = "CAM-01"
TELEMETRY_FILE = os.path.join("simulation", "cctv", "cctv_telemetry.json")

# This is intentionally a fixed, local demonstration set, not unrestricted brute force.
CONTROLLED_CREDENTIALS = (
    ("admin", "123456"),
    ("admin", "password"),
    ("admin", "admin"),
)


def main() -> int:
    print("=" * 60)
    print("        SMARTCITY-X CCTV ATTACK SIMULATION")
    print("=" * 60)
    print(f"Target Camera : {CAMERA_ID}")
    print("Attack        : Authentication + Session Compromise")

    try:
        status_response = requests.get(f"{SERVER}/api/cctv/{CAMERA_ID}", timeout=5)
        status_response.raise_for_status()
        initial = status_response.json()["data"]
    except requests.RequestException as error:
        print(f"[ERROR] Backend unavailable: {error}")
        return 1

    print(f"Initial state : {initial['authentication']} / {initial['session']} / {initial['stream']}")
    for username, password in CONTROLLED_CREDENTIALS:
        print(f"[ATTACK] Trying {username} / {password} ...")
        if username == "admin" and password == "admin":
            print("[ATTACK] SUCCESS - credentials accepted")
            break
        print("[ATTACK] FAILED")

    try:
        response = requests.post(f"{SERVER}/api/cctv/{CAMERA_ID}/attack", timeout=5)
        response.raise_for_status()
        result = response.json()["data"]
    except requests.RequestException as error:
        print(f"[ERROR] Attack could not be applied: {error}")
        return 1

    telemetry = result["telemetry"]
    os.makedirs(os.path.dirname(TELEMETRY_FILE), exist_ok=True)
    with open(TELEMETRY_FILE, "w", encoding="utf-8") as telemetry_file:
        json.dump(telemetry, telemetry_file, indent=4)

    print("[!] CCTV authentication compromised")
    print("[!] Unauthorized session established")
    print("[!] Legitimate session terminated")
    print("[!] CCTV stream interrupted")
    print(f"[+] Telemetry saved at {TELEMETRY_FILE}")
    print(f"[+] Completed at {datetime.now().isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
