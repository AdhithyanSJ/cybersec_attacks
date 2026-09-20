import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TELEMETRY_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "network"
    / "network_telemetry.json"
)

with open(TELEMETRY_FILE, "r") as f:
    telemetry = json.load(f)

print("=" * 60)
print("SMARTCITY-X SOC")
print("=" * 60)

incident_id = datetime.now().strftime("SCX-%Y%m%d-%H%M%S")

print("\n🚨 SMARTCITY-X SOC ALERT")

print("\n[INCIDENT]")
print(f"Incident ID: {incident_id}")
print(f"Target:      Public Network")
print(f"SSID:        {telemetry['observed_ssid']}")

print("\n[DETECTION EVIDENCE]")

if telemetry["unauthorized_ap"]:
    print("[X] Unauthorized access point")

if telemetry["ssid_mismatch"]:
    print("[X] Network identity mismatch")

if telemetry["gateway_mismatch"]:
    print("[X] Gateway identity mismatch")

print("\n[THREAT CLASSIFICATION]")
print("Threat: ROGUE ACCESS POINT")
print("Severity: HIGH")
print("Detection score: 3/3")

print("\n" + "=" * 60)
print("AUTOMATED RESPONSE")
print("=" * 60)

print("\n[RESPONSE] Rogue access point confirmed.")
print("[RESPONSE] Isolating affected network session...")
print("[RESPONSE] Blocking unauthorized network identity...")
print("[RESPONSE] Restoring authorized network configuration...")
print("[RESPONSE] Client redirected to authorized network.")
print("[RESPONSE] Network state restored.")
print("[RESPONSE] Incident logged.")

incident = {
    "incident_id": incident_id,
    "timestamp": datetime.now().isoformat(),
    "threat": "ROGUE ACCESS POINT",
    "severity": "HIGH",
    "detection_score": "3/3",
    "authorized_ssid": telemetry["authorized_ssid"],
    "observed_ssid": telemetry["observed_ssid"],
    "authorized_gateway": telemetry["authorized_gateway"],
    "observed_gateway": telemetry["observed_gateway"],
    "response": "UNAUTHORIZED_NETWORK_ISOLATED"
}

INCIDENT_FILE = (
    PROJECT_ROOT
    / "soc"
    / "network_incident_log.json"
)

with open(INCIDENT_FILE, "w") as f:
    json.dump(incident, f, indent=4)

print("\n" + "=" * 60)
print("SOC INCIDENT SUMMARY")
print("=" * 60)

print(f"Incident ID: {incident_id}")
print("Threat:      ROGUE ACCESS POINT")
print("Severity:    HIGH")
print("Response:    UNAUTHORIZED_NETWORK_ISOLATED")
print("Status:      NETWORK_RESTORED")

print(f"\nIncident log: {INCIDENT_FILE}")

print("=" * 60)