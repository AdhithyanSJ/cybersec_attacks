import json
import os
from datetime import datetime


# ============================================================
# SMARTCITY-X
# Attack #5 SOC Response
# Unauthorized Admin API Access
# ============================================================

TELEMETRY_FILE = "E:\\cybersec\\SmartCity-X\\simulation\\api\\api_telemetry.json"
INCIDENT_LOG = "E:\\cybersec\\SmartCity-X\\soc\\api_incident_log.json"


print("=" * 60)
print("             SMARTCITY-X API SOC")
print("=" * 60)


# ============================================================
# LOAD TELEMETRY
# ============================================================

if not os.path.exists(TELEMETRY_FILE):

    print()
    print("[ERROR] API telemetry not found.")
    print(f"[ERROR] Expected: {TELEMETRY_FILE}")
    exit()


try:

    with open(
        TELEMETRY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        telemetry = json.load(file)

except Exception as e:

    print()
    print("[ERROR] Could not read telemetry.")
    print(f"[ERROR] {e}")
    exit()


# ============================================================
# EXTRACT INCIDENT INFORMATION
# ============================================================

target = telemetry.get("target")
endpoint = telemetry.get("endpoint")
http_status = telemetry.get("http_status")

severity = "HIGH"

unauthorized_access = telemetry.get(
    "unauthorized_access"
)

admin_configuration_exposed = telemetry.get(
    "admin_configuration_exposed"
)

security_related_data_exposed = telemetry.get(
    "security_related_data_exposed"
)


# ============================================================
# SOC INCIDENT
# ============================================================

incident_id = (
    "SCX-API-" +
    datetime.now().strftime("%Y%m%d-%H%M%S")
)


print()
print("-" * 60)
print("                 INCIDENT DETECTED")
print("-" * 60)

print(f"Incident ID : {incident_id}")
print("Threat      : UNAUTHORIZED ADMIN API ACCESS")
print(f"Severity    : {severity}")
print(f"Target      : {target}")
print(f"Endpoint    : {endpoint}")
print(f"HTTP Status : {http_status}")


# ============================================================
# SOC ANALYSIS
# ============================================================

print()
print("-" * 60)
print("                  SOC ANALYSIS")
print("-" * 60)

if unauthorized_access:

    print("[!] Unauthorized API access confirmed")

if admin_configuration_exposed:

    print("[!] Administrative configuration exposed")

if security_related_data_exposed:

    print("[!] Security-related application data exposed")


# ============================================================
# AUTOMATED RESPONSE
# ============================================================

print()
print("-" * 60)
print("              AUTOMATED RESPONSE")
print("-" * 60)

print("[RESPONSE] Suspicious API request identified.")
print("[RESPONSE] Unauthorized API session contained.")
print("[RESPONSE] Suspicious API access blocked.")
print("[RESPONSE] Session access revoked.")
print("[RESPONSE] Administrative endpoint access isolated.")


response = "API_ACCESS_CONTAINED"

print()
print(f"Response: {response}")


# ============================================================
# INCIDENT LOG
# ============================================================

incident_log = {

    "incident_id": incident_id,

    "timestamp": datetime.now().isoformat(),

    "threat": "UNAUTHORIZED ADMIN API ACCESS",

    "severity": severity,

    "target": target,

    "endpoint": endpoint,

    "method": telemetry.get("method"),

    "http_status": http_status,

    "authorization_header":
        telemetry.get("authorization_header"),

    "admin_configuration_exposed":
        admin_configuration_exposed,

    "security_related_data_exposed":
        security_related_data_exposed,

    "detection_indicators": 6,

    "response": response,

    "status": "CONTAINED",

    "response_type": "SIMULATED_SOC_RESPONSE"
}


# ============================================================
# SAVE INCIDENT
# ============================================================

try:

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

except Exception as e:

    print()
    print("[ERROR] Could not write incident log.")
    print(f"[ERROR] {e}")
    exit()


# ============================================================
# FINAL STATUS
# ============================================================

print()
print("-" * 60)
print("                  SOC RESPONSE")
print("-" * 60)

print("[RESPONSE] API access contained.")
print("[RESPONSE] Suspicious session revoked.")
print("[RESPONSE] Incident logged.")

print()
print(f"Response: {response}")
print("Final State: API ACCESS CONTAINED")
print(f"Incident Log: {INCIDENT_LOG}")

print()
print("=" * 60)
print("                API SOC COMPLETE")
print("=" * 60)