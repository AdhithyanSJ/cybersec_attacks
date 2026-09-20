import json
import os
import requests
from datetime import datetime


# ============================================================
# SMARTCITY-X
# CCTV SOC RESPONSE
# ============================================================

TELEMETRY_FILE = "simulation/cctv/cctv_telemetry.json"

INCIDENT_LOG = "soc/cctv_incident_log.json"

SERVER = "http://127.0.0.1:5001"


print("=" * 60)
print("             SMARTCITY-X CCTV SOC")
print("=" * 60)


# ============================================================
# LOAD TELEMETRY
# ============================================================

if not os.path.exists(TELEMETRY_FILE):

    print("[ERROR] CCTV telemetry not found.")

    exit()


with open(
    TELEMETRY_FILE,
    "r",
    encoding="utf-8"
) as file:

    telemetry = json.load(file)


camera_id = telemetry.get(
    "camera_id"
)


incident_id = (
    "SCX-CCTV-" +
    datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )
)


# ============================================================
# INCIDENT
# ============================================================

print()

print("-" * 60)
print("                 INCIDENT DETECTED")
print("-" * 60)

print(f"Incident ID : {incident_id}")

print(
    "Threat      : "
    "CCTV AUTHENTICATION AND SESSION COMPROMISE"
)

print("Severity    : HIGH")

print(
    f"Camera      : {camera_id}"
)

print(
    f"Location    : "
    f"{telemetry.get('camera_location')}"
)


# ============================================================
# SOC ANALYSIS
# ============================================================

print()

print("-" * 60)
print("                  SOC ANALYSIS")
print("-" * 60)

print(
    "[!] Authentication attack confirmed"
)

print(
    "[!] Unauthorized camera session confirmed"
)

print(
    "[!] Legitimate session terminated"
)

print(
    "[!] CCTV stream interruption confirmed"
)


# ============================================================
# AUTOMATED RESPONSE
# ============================================================

print()

print("-" * 60)
print("              AUTOMATED RESPONSE")
print("-" * 60)

print(
    "[RESPONSE] Identifying unauthorized session..."
)

print(
    "[RESPONSE] Revoking attacker session..."
)


# ============================================================
# RESTORE CAMERA
# ============================================================

try:

    response = requests.post(
        f"{SERVER}/api/cctv/{camera_id}/reset",
        timeout=5
    )

    if response.status_code == 200:

        print(
            "[RESPONSE] Legitimate camera session restored"
        )

        print(
            "[RESPONSE] CCTV stream restored"
        )

        response_status = (
            "CAMERA_SESSION_RESTORED"
        )

        final_state = "CAMERA RESTORED"

    else:

        print(
            "[ERROR] Camera restoration failed"
        )

        response_status = (
            "CAMERA_RESTORE_FAILED"
        )

        final_state = "CAMERA COMPROMISED"


except requests.RequestException as e:

    print(
        "[ERROR] Could not contact CCTV server"
    )

    print(e)

    response_status = (
        "CAMERA_RESTORE_FAILED"
    )

    final_state = "CAMERA COMPROMISED"


# ============================================================
# INCIDENT LOG
# ============================================================

incident_log = {

    "incident_id":
        incident_id,

    "timestamp":
        datetime.now().isoformat(),

    "threat":
        "CCTV AUTHENTICATION AND SESSION COMPROMISE",

    "severity":
        "HIGH",

    "camera_id":
        camera_id,

    "camera_location":
        telemetry.get(
            "camera_location"
        ),

    "authentication_failures":
        telemetry.get(
            "authentication_failures"
        ),

    "unauthorized_session":
        telemetry.get(
            "unauthorized_session"
        ),

    "legitimate_session_terminated":
        telemetry.get(
            "legitimate_session_terminated"
        ),

    "stream_interrupted":
        telemetry.get(
            "stream_interrupted"
        ),

    "response":
        response_status,

    "status":
        "CONTAINED"
        if response_status ==
        "CAMERA_SESSION_RESTORED"
        else "RESTORATION_FAILED",

    "response_type":
        "SIMULATED_SOC_RESPONSE"
}


os.makedirs(
    "soc",
    exist_ok=True
)


with open(
    INCIDENT_LOG,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        incident_log,
        file,
        indent=4
    )


# ============================================================
# FINAL STATUS
# ============================================================

print()

print("-" * 60)
print("                  SOC RESPONSE")
print("-" * 60)

print(
    "[RESPONSE] Attacker session revoked."
)

print(
    "[RESPONSE] Legitimate session restored."
)

print(
    "[RESPONSE] CCTV stream restored."
)

print(
    "[RESPONSE] Incident logged."
)

print()

print(
    f"Response: {response_status}"
)

print(
    f"Final State: {final_state}"
)

print(
    f"Incident Log: {INCIDENT_LOG}"
)

print()

print("=" * 60)
print("               CCTV SOC COMPLETE")
print("=" * 60)